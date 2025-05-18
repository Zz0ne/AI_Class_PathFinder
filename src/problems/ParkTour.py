from searchAlgorithms.helpers.HeuristicProblem import HeuristicProblem
from searchAlgorithms.helpers.Node import Node
from dataclasses import dataclass


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@dataclass(frozen=True)
class TourState:
    coordinates: tuple[int, int]  # Posição atual no parque (x, y)
    guideLeft: bool  # Indica se a equipa de resgate já saiu do parque
    timeLeft: int  # Unidades de tempo restantes
    satisfaction: int
    visited: frozenset[tuple[int, int]]


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
        placeHolder = TourState((0, 0), False, 0, 0, frozenset([]))
        super().__init__(placeHolder, placeHolder)

        self._park = park
        self._parkSize = size
        self._time = time
        self._idealSatisfaction = time + pointsOfInterestTotal

        self._pointsOfInterestTotal = pointsOfInterestTotal
        self._pointsOfInterestNumber = pointsOfInterestNumber

        self._pointsOfInterestMap = self._gereratePointsOfInterestMap()
        self._exitDistanceMap = self._generateExitDistanceMap()

        self._satisfactionPenalty = 0

        self._goalNode: Node | None = None
        self._expansions = 0

    def _gereratePointsOfInterestMap(self):
        pois = [
            (i, j)
            for i, row in enumerate(self._park)
            for j, val in enumerate(row)
            if val < 0
        ]

        distMap = {}

        for y in range(self._parkSize):
            for x in range(self._parkSize):
                # compute distance to each POI
                distances = sorted(
                    [(poi, manhattan((x, y), poi)) for poi in pois],
                    key=lambda poi: poi[1],
                )
                distMap[(x, y)] = distances

        return distMap

    def _generateExitDistanceMap(self):
        """
        Para cada posição (x,y) do parque, devolve uma lista de
        (exit_coord, manhattan_distance) para cada um dos 4 portões.
        """
        # 1) coordenadas dos 4 portões (centro de cada lado)
        mid = self._parkSize // 2
        exits = [
            (mid, 0),  # porta topo
            (mid, self._parkSize - 1),  # porta base
            (0, mid),  # porta esquerda
            (self._parkSize - 1, mid),  # porta direita
        ]

        distMap = {}
        for y in range(self._parkSize):
            for x in range(self._parkSize):
                exitDistances = sorted(
                    [(exitCoord, manhattan((x, y), exitCoord)) for exitCoord in exits],
                    key=lambda exitDistance: exitDistance[1],
                )
                distMap[(x, y)] = exitDistances
        return distMap

    def _isValid(self, x, y, timeLeft):
        # Verifica se as coordenadas estão dentro do parque e não são bloqueadas por um obstáculo
        if not (0 <= x < self._parkSize and 0 <= y < self._parkSize):
            return False

        if self._park[y][x] == 10:
            return False

        # Tempo após o movimento
        newTime = timeLeft
        if self._park[y][x] > 0:
            newTime -= self._park[y][x]
        else:
            newTime -= 1

        # Distância mínima até saída, a partir do mapa
        # cada entrada é (exit_coord, dist)
        _, minDist = self._exitDistanceMap[(x, y)][0]

        if newTime < minDist:
            return False

        return True

    def _createNode(self, parent, x, y):
        # Método genérico para criar um novo Node após validar movimentos
        s: TourState = parent.state
        tileVal = self._park[y][x]

        newTime = s.timeLeft - (1 if tileVal < 0 else tileVal)
        if newTime < 0:
            return None

        newVisited = set(s.visited)
        newVisited.add((x, y))

        # Visita ponto de interesse se a célula tiver custo negativo
        newSatisfaction = s.satisfaction
        if tileVal < 0 and (x, y) not in s.visited:
            newSatisfaction += abs(tileVal) + 1
            self._satisfactionPenalty = 0
        elif (x, y) in s.visited:
            newSatisfaction -= self._satisfactionPenalty
            self._satisfactionPenalty = 1
        else:
            newSatisfaction += 1
            self._satisfactionPenalty = 0

        newState = TourState(
            (x, y), False, newTime, newSatisfaction, frozenset(newVisited)
        )
        newNode = Node(newState, parent)
        newNode.cost = self._idealSatisfaction - newSatisfaction
        return newNode

    # Os quatro métodos seguintes tratam do movimento em cada direção
    def _moveUp(self, node: Node):
        x, y = node.state.coordinates
        new_y = y - 1

        if new_y < 0:
            # Verifica se está numa saida
            if x == self._parkSize // 2:
                if node.state.timeLeft < 1:
                    return None
                return Node(
                    TourState(
                        (x, new_y),
                        True,
                        node.state.timeLeft - 1,
                        node.state.satisfaction,
                        node.state.visited,
                    ),
                    node,
                    node.cost,
                )
            return None

        if not self._isValid(x, new_y, node.state.timeLeft):
            return None

        return self._createNode(node, x, new_y)

    def _moveDown(self, node: Node):
        x, y = node.state.coordinates
        new_y = y + 1

        if new_y >= self._parkSize:
            # Verifica se está numa saida
            if x == self._parkSize // 2:
                if node.state.timeLeft < 1:
                    return None
                return Node(
                    TourState(
                        (x, new_y),
                        True,
                        node.state.timeLeft - 1,
                        node.state.satisfaction,
                        node.state.visited,
                    ),
                    node,
                    node.cost,
                )
            return None

        if not self._isValid(x, new_y, node.state.timeLeft):
            return None

        return self._createNode(node, x, new_y)

    def _moveLeft(self, node: Node):
        x, y = node.state.coordinates
        new_x = x - 1

        if new_x < 0:
            # Verifica se está numa saida
            if y == self._parkSize // 2:
                if node.state.timeLeft < 1:
                    return None
                return Node(
                    TourState(
                        (new_x, y),
                        True,
                        node.state.timeLeft - 1,
                        node.state.satisfaction,
                        node.state.visited,
                    ),
                    node,
                    node.cost,
                )
            return None

        if not self._isValid(new_x, y, node.state.timeLeft):
            return None

        return self._createNode(node, new_x, y)

    def _moveRight(self, node: Node):
        x, y = node.state.coordinates
        new_x = x + 1

        if new_x >= self._parkSize:
            # Verifica se está numa saida
            if y == self._parkSize // 2:
                if node.state.timeLeft < 1:
                    return None
                return Node(
                    TourState(
                        (new_x, y),
                        True,
                        node.state.timeLeft - 1,
                        node.state.satisfaction,
                        node.state.visited,
                    ),
                    node,
                    node.cost,
                )
            return None

        if not self._isValid(new_x, y, node.state.timeLeft):
            return None

        return self._createNode(node, new_x, y)

    def expand(self, node: Node) -> list[Node]:
        # Expande possíveis movimentos a partir do node atual

        if node.state.guideLeft:
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

        return [
            Node(TourState(gate, False, self._time, 0, frozenset([]))) for gate in gates
        ]

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
        s: TourState = node.state
        return (s.coordinates, s.satisfaction)

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
        s: TourState = node.state

        try:
            nearestPOI, _ = self._pointsOfInterestMap[s.coordinates][0]
            x, y = nearestPOI

            potentialSatisfacion = self._park[y][x]
            if s.coordinates not in s.visited:
                x, y = s.coordinates
                potentialSatisfacion = -self._park[y][x]
            else:
                potentialSatisfacion -= 1

            return max(
                (self._idealSatisfaction) - (potentialSatisfacion + s.timeLeft),
                0,
            )
        except KeyError:  # A coordenada do estado atual é uma entrada/saida
            return max((self._idealSatisfaction) - (s.satisfaction + s.timeLeft), 0)
