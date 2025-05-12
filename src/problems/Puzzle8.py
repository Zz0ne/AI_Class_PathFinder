from searchAlgorithms.helpers.HeuristicProblem import HeuristicProblem
from searchAlgorithms.helpers.Node import Node


class Puzzle8(HeuristicProblem):
    ROW_SIZE = 3
    COL_SIZE = 3

    def __init__(self, initialState: list, goalState: list):
        super().__init__(initialState, goalState)

        self._goalNode: Node | None = None

    def _moveUp(self, node: Node):
        emptyIndex = node.state.index(0)
        row = emptyIndex // self.ROW_SIZE

        # if the tile is in the first row
        if row == 0:
            return None

        newNode = Node(node.state[:], node)
        newNode.cost = node.cost + 1

        newNode.state[emptyIndex], newNode.state[emptyIndex - self.ROW_SIZE] = (
            newNode.state[emptyIndex - self.ROW_SIZE],
            newNode.state[emptyIndex],
        )

        return newNode

    def _moveDown(self, node: Node):
        emptyIndex = node.state.index(0)
        row = emptyIndex // self.ROW_SIZE

        # if the tile is in the last row
        if row == self.ROW_SIZE - 1:
            return None

        newNode = Node(node.state[:], node)
        newNode.cost = node.cost + 1

        newNode.state[emptyIndex], newNode.state[emptyIndex + self.ROW_SIZE] = (
            newNode.state[emptyIndex + self.ROW_SIZE],
            newNode.state[emptyIndex],
        )

        return newNode

    def _moveLeft(self, node: Node):
        emptyIndex = node.state.index(0)
        col = emptyIndex % self.COL_SIZE

        # if the tile is in the first col
        if col == 0:
            return None

        newNode = Node(node.state[:], node)
        newNode.cost = node.cost + 1

        newNode.state[emptyIndex], newNode.state[emptyIndex - 1] = (
            newNode.state[emptyIndex - 1],
            newNode.state[emptyIndex],
        )

        return newNode

    def _moveRight(self, node: Node):
        emptyIndex = node.state.index(0)
        col = emptyIndex % self.COL_SIZE

        # if the tile is in the first col
        if col == self.COL_SIZE - 1:
            return None

        newNode = Node(node.state[:], node)
        newNode.cost = node.cost + 1

        newNode.state[emptyIndex], newNode.state[emptyIndex + 1] = (
            newNode.state[emptyIndex + 1],
            newNode.state[emptyIndex],
        )

        return newNode

    @property
    def initialNodes(self):
        return [self._initialNode]

    @property
    def goalNode(self) -> Node | None:
        return self._goalNode

    def isGoal(self, node: Node):
        if node.state == self._goalState:
            self._goalNode = node
            return True
        return False

    def expand(self, node: Node) -> list[Node]:
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
        return tuple(node.state)

    def heuristic(self, node: Node):
        # currState: List = node.state
        # value = 0
        #
        # for i, state in enumerate(currState):
        #     if state != self._goalState[i]:
        #         value += 1
        #
        # return value
        currState = node.state
        distance = 0

        for i, tile in enumerate(currState):
            if tile == 0:
                continue

            goalIndex = self._goalState.index(tile)
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(goalIndex, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)

        return distance
