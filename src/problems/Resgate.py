from searchAlgorithms.helpers.Problem import Problem
from searchAlgorithms.helpers.Node import Node
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RescueState:
    coordinates: tuple[int, int]
    teamLeft: bool
    timeLeft: int
    rescued: set[tuple[int, int]] = field(default_factory=set)


class Rescue(Problem):
    def __init__(
        self,
        park: list[list[int]],
        size: int,
        objective: int,
        totalVictims: int,
        time: int,
    ):
        placeHolder = RescueState((0, 0), False, 0)
        super().__init__(placeHolder, placeHolder)
        self._park = park
        self._parkSize = size
        self._objective = objective
        self._totalVictims = totalVictims
        self._time = time

        self._goalNode: Node | None = None

    def _moveUp(self, node: Node):
        x, y = node.state.coordinates
        new_y = y - 1

        if new_y < 0:
            if x == self._parkSize // 2:
                timeLeft = node.state.timeLeft - 1

                if timeLeft < 0:
                    return None

                newState = RescueState((x, new_y), True, timeLeft, node.state.rescued)
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[new_y][x] == 10:
            return None

        cost = self._park[new_y][x]

        timeLeft = node.state.timeLeft
        rescued = node.state.rescued

        if cost < 0 and (x, new_y) not in rescued:
            timeLeft += abs(cost)
            rescued = rescued.union({(x, new_y)})
        else:
            timeLeft -= cost

        if timeLeft <= 0:
            return None

        newState = RescueState((x, new_y), False, timeLeft, rescued)
        newNode = Node(newState, node)
        newNode.cost = node.cost + cost
        return newNode

    def _moveDown(self, node: Node):
        x, y = node.state.coordinates
        new_y = y + 1

        if new_y >= self._parkSize:
            if x == self._parkSize // 2:
                timeLeft = node.state.timeLeft - 1
                if timeLeft < 0:
                    return None
                newState = RescueState((x, new_y), True, timeLeft, node.state.rescued)
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[new_y][x] == 10:
            return None

        cost = self._park[new_y][x]
        timeLeft = node.state.timeLeft
        rescued = node.state.rescued

        if cost < 0 and (x, new_y) not in rescued:
            timeLeft += abs(cost)
            rescued = rescued.union({(x, new_y)})
        else:
            timeLeft -= cost

        if timeLeft <= 0:
            return None

        newState = RescueState((x, new_y), False, timeLeft, rescued)
        newNode = Node(newState, node)
        newNode.cost = node.cost + cost
        return newNode

    def _moveLeft(self, node: Node):
        x, y = node.state.coordinates
        new_x = x - 1

        if new_x < 0:
            if y == self._parkSize // 2:
                timeLeft = node.state.timeLeft - 1
                if timeLeft < 0:
                    return None
                newState = RescueState((new_x, y), True, timeLeft, node.state.rescued)
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[y][new_x] == 10:
            return None

        cost = self._park[y][new_x]
        timeLeft = node.state.timeLeft
        rescued = node.state.rescued

        if cost < 0 and (new_x, y) not in rescued:
            timeLeft += abs(cost)
            rescued = rescued.union({(new_x, y)})
        else:
            timeLeft -= cost

        if timeLeft <= 0:
            return None

        newState = RescueState((new_x, y), False, timeLeft, rescued)
        newNode = Node(newState, node)
        newNode.cost = node.cost + cost
        return newNode

    def _moveRight(self, node: Node):
        x, y = node.state.coordinates
        new_x = x + 1

        if new_x == self._parkSize:
            if y == self._parkSize // 2:
                timeLeft = node.state.timeLeft - 1
                if timeLeft < 0:
                    return None
                newState = RescueState((new_x, y), True, timeLeft, node.state.rescued)
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[y][new_x] == 10:
            return None

        cost = self._park[y][new_x]
        timeLeft = node.state.timeLeft
        rescued = node.state.rescued

        if cost < 0 and (new_x, y) not in rescued:
            timeLeft += abs(cost)
            rescued = rescued.union({(new_x, y)})
        else:
            timeLeft -= cost

        if timeLeft <= 0:
            return None

        newState = RescueState((new_x, y), False, timeLeft, rescued)
        newNode = Node(newState, node)
        newNode.cost = node.cost + cost
        return newNode

    @property
    def initialNodes(self):
        middle = self._parkSize // 2
        size = self._parkSize

        gates = [(middle, size - 1), (middle, 0), (0, middle), (size - 1, middle)]

        initialNodes = []

        for gate in gates:
            initialState = RescueState(gate, False, self._time)
            node = Node(initialState)
            initialNodes.append(node)

        return initialNodes

    @property
    def goalState(self):
        return self._goalState

    @property
    def goalNode(self) -> Node | None:
        return self._goalNode

    def isGoal(self, node: Node) -> bool:
        s: RescueState = node.state

        if s.timeLeft <= 0:
            return False

        if len(s.rescued) != self._objective:
            return False

        if not s.teamLeft:
            return False

        self._goalNode = node
        return True

    def expand(self, node: Node) -> list[Node]:
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

        return sorted(expandedNodes)

    def hashableState(self, node: Node):
        s = node.state
        return (s.coordinates, tuple(sorted(s.rescued)))

    def printSolution(self):
        currNode = self.goalNode
        path = []

        while currNode:
            path.append(currNode.state.coordinates)
            # print(currNode.state.coordinates, currNode.state.timeLeft)
            currNode = currNode.parent
        # print()

        path = path[::-1]
        path_set = set(path)

        last_x, last_y = path[-1]

        # Determine entrance direction based on first move
        first_x, first_y = path[0]
        if first_y < 0:
            entrance_symbol = "(^)"
        elif first_y >= self._parkSize:
            entrance_symbol = "(v)"
        elif first_x < 0:
            entrance_symbol = "(<)"
        elif first_x >= self._parkSize:
            entrance_symbol = "(>)"
        else:
            entrance_symbol = "(E)"

        # Determine exit symbol
        exit_symbol = ""
        if last_y < 0:
            exit_symbol = "(^)"
        elif last_y >= self._parkSize:
            exit_symbol = "(v)"
        elif last_x < 0:
            exit_symbol = "(<)"
        elif last_x >= self._parkSize:
            exit_symbol = "(>)"

        print(f"Passos: {len(path) - 1}")
        print("*" + "---" * self._parkSize + "*")

        for y in range(self._parkSize):
            row = "|"
            for x in range(self._parkSize):
                coord = (x, y)
                tile = self._park[y][x]

                if coord == path[0]:
                    row += entrance_symbol
                elif coord in path_set:
                    if tile < 0 and coord in self.goalNode.state.rescued:
                        row += f"({-tile})"
                    elif tile == 2:
                        row += "(:)"
                    else:
                        row += "(.)"
                elif tile == 10:
                    row += " # "
                elif tile < 0:
                    row += f" {-tile} "
                elif tile == 2:
                    row += " : "
                elif tile == 1:
                    row += " . "
                else:
                    row += " . "
            row += "|"
            print(row)

        print("*" + "---" * self._parkSize + "*")

        if exit_symbol and (last_x, last_y) not in path_set:
            print(" " * (3 * last_x + 1) + exit_symbol)

        print(
            f"Tempo: {self.goalNode.state.timeLeft} ({len(self.goalNode.state.rescued)}/{self._totalVictims}), custo {self.goalNode.cost}"
        )
