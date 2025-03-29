from .helpers.Problem import Problem

import heapq
from collections import deque


def print_puzzle(state: list[int]):
    """Prints the 8-puzzle state in a 3x3 grid format."""
    ROW_SIZE = 3  # Fixed for 8-puzzle

    for i in range(ROW_SIZE):
        row = state[i * ROW_SIZE : (i + 1) * ROW_SIZE]  # Get row slice
        print(" | ".join(str(num) if num != 0 else " " for num in row))  # Format output
        if i < ROW_SIZE - 1:
            print("-" * 9)  # Row separator


def uniformCostSearch(problem: Problem):
    initialNode = problem.initialNode

    frontier = []
    heapq.heappush(frontier, initialNode)

    reached = {problem.hashableState(initialNode): initialNode.cost}

    while frontier:
        currNode = heapq.heappop(frontier)

        if problem.isGoal(currNode):
            return True

        for childNode in problem.expand(currNode):
            stateKey = problem.hashableState(childNode)

            if (stateKey not in reached) or (childNode.cost < reached[stateKey]):
                reached[stateKey] = childNode.cost
                heapq.heappush(frontier, childNode)

    return False


def depthFirstSearch(problem: Problem):
    initialNode = problem.initialNode

    frontier = [initialNode]

    reached = {problem.hashableState(initialNode): initialNode.cost}

    while frontier:
        currNode = frontier.pop()

        if problem.isGoal(currNode):
            return True

        for childNode in problem.expand(currNode):
            stateKey = problem.hashableState(childNode)

            if (stateKey not in reached) or (childNode.cost < reached[stateKey]):
                reached[stateKey] = childNode.cost
                frontier.append(childNode)

    return False


def depthLimitedSearch(problem, limit):
    initialNode = problem.initialNode
    frontier = [(initialNode, 0)]  # (node, depth)
    reached = {problem.hashableState(initialNode): initialNode.cost}

    while frontier:
        currNode, currDepth = frontier.pop()

        if problem.isGoal(currNode):
            return True

        if currDepth < limit:
            for childNode in problem.expand(currNode):
                stateKey = problem.hashableState(childNode)

                if (stateKey not in reached) or (childNode.cost < reached[stateKey]):
                    reached[stateKey] = childNode.cost
                    frontier.append((childNode, currDepth + 1))

    return False


def iterativeDeepeningSearch(problem, maxDepth=50):
    for depth in range(maxDepth):
        result = depthLimitedSearch(problem, depth)
        if result:
            return True
    return False


def breadthFirstSearch(problem: Problem):
    initialNode = problem.initialNode

    frontier = deque([initialNode])

    reached = {problem.hashableState(initialNode): initialNode.cost}

    while frontier:
        currNode = frontier.popleft()

        if problem.isGoal(currNode):
            return True

        for childNode in problem.expand(currNode):
            stateKey = problem.hashableState(childNode)

            if (stateKey not in reached) or (childNode.cost < reached[stateKey]):
                reached[stateKey] = childNode.cost
                frontier.append(childNode)

    return False
