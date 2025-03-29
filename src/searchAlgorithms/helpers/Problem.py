from .Node import Node


class Problem:
    def __init__(self, initialState, goalState):
        self._initialState = initialState
        self._goalState = goalState

        self._initialNode = Node(self._initialState)

    @property
    def initialState(self):
        return self._initialState

    @property
    def initialNode(self):
        return self._initialNode

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
