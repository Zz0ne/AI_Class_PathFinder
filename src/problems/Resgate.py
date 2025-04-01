from ..searchAlgorithms.helpers.Problem import Problem
from searchAlgorithms.helpers.Node import Node
from dataclasses import dataclass


@dataclass(frozen=True)
class RescueState:
    peopleRescued: int
    coordinates: tuple
    teamLeft: bool
    timeLeft: int


class Rescue(Problem):
    def __init__(
        self,
        initialState: RescueState,
        goalState: RescueState,
        park: list[list[int]],
        objective: int,
        totalVictims: int,
    ):
        super().__init__(initialState, goalState)
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

                newState = RescueState(
                    node.state.peopleRescued, (x, new_y), True, timeLeft
                )
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[new_y][x] == 10:
            return None

        cost = self._park[new_y][x]
        timeLeft = node.state.timeLeft - cost

        if timeLeft < 0:
            return None

        peopleRescued = node.state.peopleRescued + (cost < 0)

        newState = RescueState(peopleRescued, (x, new_y), False, timeLeft)
        newNode = Node(newState, node)
        newNode.cost = node.cost + cost
        return newNode

    def _moveDown(self, node: Node):
        x, y = node.state.coordinates
        new_y = y + 1

        if new_y == self._parkSize:
            if x == self._parkSize // 2:
                timeLeft = node.state.timeLeft - 1

                if timeLeft < 0:
                    return None

                newState = RescueState(
                    node.state.peopleRescued, (x, new_y), True, timeLeft
                )
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[new_y][x] == 10:
            return None

        cost = self._park[new_y][x]
        timeLeft = node.state.timeLeft - cost

        if timeLeft < 0:
            return None

        peopleRescued = node.state.peopleRescued + (cost < 0)

        newState = RescueState(peopleRescued, (x, new_y), False, timeLeft)
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

                newState = RescueState(
                    node.state.peopleRescued, (new_x, y), True, timeLeft
                )
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[y][new_x] == 10:
            return None

        cost = self._park[y][new_x]
        timeLeft = node.state.timeLeft - cost

        if timeLeft < 0:
            return None

        peopleRescued = node.state.peopleRescued + (cost < 0)

        newState = RescueState(peopleRescued, (new_x, y), False, timeLeft)
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

                newState = RescueState(
                    node.state.peopleRescued, (new_x, y), True, timeLeft
                )
                newNode = Node(newState, node)
                newNode.cost = node.cost + 1
                return newNode
            else:
                return None

        if self._park[y][new_x] == 10:
            return None

        cost = self._park[y][new_x]
        timeLeft = node.state.timeLeft - cost

        if timeLeft < 0:
            return None

        peopleRescued = node.state.peopleRescued + (cost < 0)

        newState = RescueState(peopleRescued, (new_x, y), False, timeLeft)
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
        s = node.state

        if s.peopleRescued != self._objective:
            return False

        if not s.teamLeft:
            return False

        if s.timeLeft < 0:
            return False

        self._goalNode = node
        return True

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
        return node.state
