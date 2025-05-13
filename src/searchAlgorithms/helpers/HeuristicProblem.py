from .Problem import Problem
from .Node import Node


class HeuristicProblem(Problem):
    def __init__(self, initialState, goalState) -> None:
        super().__init__(initialState, goalState)

    def heuristic(self, node: Node):
        raise NotImplementedError("heuristic must be implemented in a subclass")

    def g(self, node: Node):
        raise NotImplementedError("g must be implemented in a subclass")
