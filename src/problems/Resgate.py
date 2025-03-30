from ..searchAlgorithms.helpers.Problem import Problem
from searchAlgorithms.helpers.Node import Node


class Resgate(Problem):
    def __init__(self, initialState, goalState, objective, totalVictims, time):
        super().__init__(initialState, goalState)
        self._objective = objective
        self._totalVictims = totalVictims
        self._timeLeft = time

        self._goalNode: Node | None = None

    def _moveUp(self, node: Node):
        pass

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
