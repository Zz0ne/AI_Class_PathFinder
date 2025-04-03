from searchAlgorithms.helpers.Problem import Problem
from searchAlgorithms.helpers.Node import Node
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RescueState:
    coordinates: tuple[int, int]
    teamLeft: bool
    timeLeft: int
    rescued: frozenset[tuple[int, int]] = field(default_factory=frozenset)


class Rescue(Problem):
    def __init__(
        self,
        initialState: RescueState,
        park: list[list[int]],
        objective: int,
        totalVictims: int,
    ):
        placeHolder = RescueState((0, 0), False, 0)
        super().__init__(initialState, placeHolder)
        self._park = park
        self._parkSize = len(park)
        self._objective = objective
        self._totalVictims = totalVictims

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
            if timeLeft < 0:
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
            if timeLeft < 0:
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
            if timeLeft < 0:
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
            if timeLeft < 0:
                return None

        newState = RescueState((new_x, y), False, timeLeft, rescued)
        newNode = Node(newState, node)
        newNode.cost = node.cost + cost
        return newNode

    @property
    def goalState(self):
        return self._goalState

    @property
    def goalNode(self) -> Node | None:
        return self._goalNode

    def isGoal(self, node: Node) -> bool:
        s: RescueState = node.state

        if len(s.rescued) != self._objective:
            return False

        if not s.teamLeft:
            return False

        if s.timeLeft < 0:
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

        return expandedNodes

    def hashableState(self, node: Node):
        return node.state

    def printSolution(self):
        currNode = self.goalNode

        print("---Start---")
        while currNode:
            print(currNode.state.coordinates, end=" ")
            currNode = currNode.parent

        print("\n---End---")
