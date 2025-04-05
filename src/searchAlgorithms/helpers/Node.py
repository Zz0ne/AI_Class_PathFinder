from typing import Any


class Node:
    def __init__(self, state: Any, parent=None, cost: int = 0):
        if not isinstance(parent, Node | None):
            raise TypeError("Parent is not of type Node")

        self.parent: Node | None = parent
        self.state: Any = state
        self.cost = cost

    def __lt__(self, other) -> int:
        return self.cost < other.cost
