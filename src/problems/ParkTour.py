from searchAlgorithms.helpers.HeuristicProblem import HeuristicProblem
from searchAlgorithms.helpers.Node import Node
from dataclasses import dataclass


@dataclass(frozen=True)
class TourState:
    coordinates: tuple[int, int]  # Posição atual no parque (x, y)
    guideLeft: bool  # Indica se a equipa de resgate já saiu do parque
    timeLeft: int  # Unidades de tempo restantes
    satisfaction: int


class ParkTour(HeuristicProblem):
    def __init__(
        self,
        park: list[list[int]],
        size: int,
        pointsOfInterestNumber: int,
        pointsOfInterestTotal: int,
        time: int,
    ):
        # Estado inicial de placeholder para inicialização da superclasse
        placeHolder = TourState((0, 0), False, 0, 0)
        super().__init__(placeHolder, placeHolder)

        self._park = park
        self._parkSize = size
        self._pointsOfInterestTotal = pointsOfInterestTotal
        self._pointsOfInterestNumber = pointsOfInterestNumber
        self._time = time
        self._idealSatisfaction = time + pointsOfInterestTotal

        self._visitedTile: set[tuple[int, int]] = set()

        self._satisfactionPenalty = 0

        self._goalNode: Node | None = None
        self._expansions = 0

    def _isValid(self, x, y):
        # Verifica se as coordenadas estão dentro do parque e não são bloqueadas por um obstáculo
        return (
            0 <= x < self._parkSize
            and 0 <= y < self._parkSize
            and self._park[y][x] != 10
        )

    def _createNode(self, node, x, y):
        # Método genérico para criar um novo Node após validar movimentos
        cost = self._park[y][x]
        timeLeft = node.state.timeLeft
        satisfaction = node.state.satisfaction

        # Visita ponto de interesse se a célula tiver custo negativo
        if cost < 0 and (x, y) not in self._visitedTile:
            satisfaction += abs(cost)
            self._satisfactionPenalty = 0
        elif (x, y) in self._visitedTile:
            timeLeft -= 1
            satisfaction -= self._satisfactionPenalty
            self._satisfactionPenalty = 1
        else:
            timeLeft -= 1
            satisfaction += 1
            self._satisfactionPenalty = 0

        if timeLeft <= 0:
            return None

        self._visitedTile.add((x, y))

        newState = TourState((x, y), False, timeLeft, satisfaction)
        newNode = Node(newState, node)
        newNode.cost = node.cost + abs(cost)
        return newNode

    # Os quatro métodos seguintes tratam do movimento em cada direção
    def _moveUp(self, node: Node):
        x, y = node.state.coordinates
        new_y = y - 1

        if new_y < 0:
            # Verifica se está numa saida
            if x == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    TourState(
                        (x, new_y), True, node.state.timeLeft - 1, node.state.rescued
                    ),
                    node,
                    node.cost + 1,
                )
            return None

        if not self._isValid(x, new_y):
            return None

        return self._createNode(node, x, new_y)

    def _moveDown(self, node: Node):
        x, y = node.state.coordinates
        new_y = y + 1

        if new_y >= self._parkSize:
            # Verifica se está numa saida
            if x == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    TourState(
                        (x, new_y), True, node.state.timeLeft - 1, node.state.rescued
                    ),
                    node,
                    node.cost + 1,
                )
            return None

        if not self._isValid(x, new_y):
            return None

        return self._createNode(node, x, new_y)

    def _moveLeft(self, node: Node):
        x, y = node.state.coordinates
        new_x = x - 1

        if new_x < 0:
            # Verifica se está numa saida
            if y == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    TourState(
                        (new_x, y), True, node.state.timeLeft - 1, node.state.rescued
                    ),
                    node,
                    node.cost + 1,
                )
            return None

        if not self._isValid(new_x, y):
            return None

        return self._createNode(node, new_x, y)

    def _moveRight(self, node: Node):
        x, y = node.state.coordinates
        new_x = x + 1

        if new_x >= self._parkSize:
            # Verifica se está numa saida
            if y == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    TourState(
                        (new_x, y), True, node.state.timeLeft - 1, node.state.rescued
                    ),
                    node,
                    node.cost + 1,
                )
            return None

        if not self._isValid(new_x, y):
            return None

        return self._createNode(node, new_x, y)

    def expand(self, node: Node) -> list[Node]:
        # Expande possíveis movimentos a partir do node atual

        if node.state.teamLeft:
            return []

        newNodes = []

        upNode = self._moveUp(node)
        if upNode:
            newNodes.append(upNode)

        downNode = self._moveDown(node)
        if downNode:
            newNodes.append(downNode)

        leftNode = self._moveLeft(node)
        if leftNode:
            newNodes.append(leftNode)

        rightNode = self._moveRight(node)
        if rightNode:
            newNodes.append(rightNode)

        self._expansions += 1
        return newNodes

    @property
    def initialNodes(self):
        # Pontos de entrada nas quatro direções do parque
        middle = self._parkSize // 2
        gates = [
            (middle, self._parkSize - 1),
            (middle, 0),
            (0, middle),
            (self._parkSize - 1, middle),
        ]

        return [Node(TourState(gate, False, self._time, 0)) for gate in gates]

    @property
    def goalNode(self):
        return self._goalNode

    @goalNode.setter
    def goalNode(self, node: Node):
        self._goalNode = node

    def isGoal(self, node: Node) -> bool:
        # Verifica condições do objetivo
        s = node.state
        return s.guideLeft and s.timeLeft == 0

    def getResultData(self):
        # Devolve métricas do resultado se for encontrado um node objetivo
        if self._goalNode:
            currNode = self._goalNode
            generations = 0
            while currNode:
                generations += 1
                currNode = currNode.parent
            return (
                self._goalNode.cost,
                self._expansions,
                generations,
                self._goalNode.state.satisfaction,
                self._goalNode.state.timeLeft,
            )

    def hashableState(self, node: Node):
        # Cria identificador único para cada estado
        s = node.state
        return (s.coordinates, tuple(sorted(s.rescued)))

    def getPath(self):
        # Devolve o caminho da solução
        currNode = self._goalNode
        path = []
        while currNode:
            path.append(currNode.state.coordinates)
            currNode = currNode.parent

        return path[::-1]

    def heuristic(self, node: Node):
        """
        Heurística admissível que subestima o custo restante para atingir a satisfação ideal,
        ignorando possíveis ganhos adicionais de pontos de interesse ainda não visitados.
        """

        s = node.state

        return max(
            (self._idealSatisfaction) - (s.satisfaction + s.timeLeft),
            0,
        )
