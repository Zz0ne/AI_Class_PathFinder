from .helpers.Problem import Problem

import heapq
from collections import deque


def uniformCostSearch(problem: Problem):
    initialNodes = problem.initialNodes

    frontier = []
    for node in initialNodes:
        heapq.heappush(frontier, node)

    reached = {problem.hashableState(node): node.cost for node in initialNodes}

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
    initialNodes = problem.initialNodes

    frontier = initialNodes[:]

    reached = {problem.hashableState(node): node.cost for node in initialNodes}

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


def depthLimitedSearch(problem: Problem, limit: int):
    initialNodes = problem.initialNodes

    frontier = [(node, 0) for node in initialNodes]
    reached = {problem.hashableState(node): node.cost for node in initialNodes}

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
    initialNodes = problem.initialNodes

    frontier = deque(initialNodes)

    reached = {problem.hashableState(node): node.cost for node in initialNodes}

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
