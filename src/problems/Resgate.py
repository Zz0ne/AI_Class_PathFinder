from searchAlgorithms.helpers.Problem import Problem
from searchAlgorithms.helpers.Node import Node
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RescueState:
    coordinates: tuple[int, int]  # Posição atual no parque (x, y)
    teamLeft: bool  # Indica se a equipa de resgate já saiu do parque
    timeLeft: int  # Unidades de tempo restantes
    rescued: frozenset[tuple[int, int]] = field(
        default_factory=frozenset
    )  # Conjunto das coordenadas das pessoas resgatadas


class Rescue(Problem):
    def __init__(
        self,
        park: list[list[int]],
        size: int,
        objective: int,
        totalVictims: int,
        time: int,
    ):
        # Estado inicial de placeholder para inicialização da superclasse
        placeHolder = RescueState((0, 0), False, 0)
        super().__init__(placeHolder, placeHolder)

        self._park = park
        self._parkSize = size
        self._objective = objective
        self._totalVictims = totalVictims
        self._time = time

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
        rescued = node.state.rescued

        # Resgata pessoas se a célula tiver custo negativo
        if cost < 0 and (x, y) not in rescued:
            timeLeft += abs(cost)
            rescued = rescued.union({(x, y)})
        else:
            timeLeft -= cost

        if timeLeft <= 0:
            return None

        newState = RescueState((x, y), False, timeLeft, rescued)
        newNode = Node(newState, node)
        newNode.cost = node.cost + abs(cost)
        return newNode

    # Os quatro métodos seguintes tratam do movimento em cada direção
    def _moveUp(self, node: Node):
        x, y = node.state.coordinates
        new_y = y - 1

        if new_y < 0:
            if x == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    RescueState(
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
            if x == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    RescueState(
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
            if y == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    RescueState(
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
            if y == self._parkSize // 2:
                if node.state.timeLeft <= 1:
                    return None
                return Node(
                    RescueState(
                        (new_x, y), True, node.state.timeLeft - 1, node.state.rescued
                    ),
                    node,
                    node.cost + 1,
                )
            return None

        if not self._isValid(new_x, y):
            return None

        return self._createNode(node, new_x, y)

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

        return [Node(RescueState(gate, False, self._time)) for gate in gates]

    def getResultData(self):
        # Devolve métricas do resultado se for encontrado um node objetivo
        if self._goalNode:
            currNode = self._goalNode
            generations = 0
            while currNode:
                generations += 1
                currNode = currNode.parent
            return self._goalNode.cost, self._expansions, generations

    def isGoal(self, node: Node) -> bool:
        # Verifica condições do objetivo
        s = node.state
        if not s.teamLeft or len(s.rescued) != self._objective or s.timeLeft <= 0:
            return False
        self._goalNode = node
        return True

    def expand(self, node: Node) -> list[Node]:
        # Expande possíveis movimentos a partir do node atual

        if node.state.teamLeft:
            return []

        expandedNodes = []

        upNode = self._moveUp(node)
        if upNode:
            expandedNodes.append(upNode)

        downNode = self._moveDown(node)
        if downNode:
            expandedNodes.append(downNode)

        leftNode = self._moveLeft(node)
        if leftNode:
            expandedNodes.append(leftNode)

        rightNode = self._moveRight(node)
        if rightNode:
            expandedNodes.append(rightNode)

        self._expansions += 1
        return expandedNodes

    def hashableState(self, node: Node):
        # Cria identificador único para cada estado
        s = node.state
        return (s.coordinates, tuple(sorted(s.rescued)))

    def printSolution(self):
        # Imprime o caminho da solução e informações relevantes
        currNode = self.goalNode
        path = []
        while currNode:
            path.append(currNode.state.coordinates)
            currNode = currNode.parent

        path = path[::-1]
        print(f"Solução encontrada: {path}")
