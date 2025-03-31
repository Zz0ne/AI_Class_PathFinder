from ..searchAlgorithms.helpers.Problem import Problem
from searchAlgorithms.helpers.Node import Node


class RescueState:
    def __init__(self):
        self.peopleRescued = 0
        self.coordinates = (0, 0)
        self.teamLeft = False
        self.timeLeft = 0


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
        cost = 0
        teamLeft = False

        x, y = node.state.coordinates
        y -= 1

        if y < 0:
            if x == self._parkSize // 2:
                cost = 1
                teamLeft = True
        else:
            return None

        if self._park[y][x] == 10:
            return None

        cost = self._park[y][x]

        newState = RescueState()
        newState.timeLeft -= cost
        if newState.timeLeft >= 0:
            return None

        newState.peopleRescued += cost < 0
        newState.coordinates = (x, y)
        newState.teamLeft = teamLeft

        newNode = Node(newState, node)
        newNode.cost = node.cost + cost
        return newNode

    def _moveDown(self, node: Node):
        pass

    def _moveLeft(self, node: Node):
        pass

    def _moveRight(self, node: Node):
        pass

    @property
    def goalState(self):
        return self._goalState

    @property
    def goalNode(self) -> Node | None:
        raise NotImplementedError("goalNode must be implemented in a subclass")

    def isGoal(self, node: Node) -> bool:
        raise NotImplementedError("isGoal must be implemented in a subclass")

    def expand(self, node: Node) -> list[Node]:
        raise NotImplementedError("expand must be implemented in a subclass")

    def hashableState(self, node: Node):
        raise NotImplementedError("hashState must be implemented in a subclass")
