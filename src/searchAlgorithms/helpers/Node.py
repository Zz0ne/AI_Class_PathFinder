from typing import Any


class Node:
    def __init__(
        self,
        state: Any,
        parent=None,
    ):
        if not isinstance(parent, Node | None):
            raise TypeError("Parent is not of type Node")

        self.parent: Node | None = parent
        self.state: Any = state
        self.cost = 0

    def __lt__(self, other) -> int:
        return self.cost < other.cost
