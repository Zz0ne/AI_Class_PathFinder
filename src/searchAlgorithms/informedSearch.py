from .helpers.HeuristicProblem import HeuristicProblem

import heapq


def bestFirstSearch(problem: HeuristicProblem):
    initialNodes = problem.initialNodes

    frontier = []
    for node in initialNodes:
        heapq.heappush(frontier, (problem.heuristic(node), node))

    reached = {problem.hashableState(node): node.cost for node in initialNodes}

    while frontier:
        _, currNode = heapq.heappop(frontier)

        if problem.isGoal(currNode):
            return True

        for childNode in problem.expand(currNode):
            stateKey = problem.hashableState(childNode)

            if (stateKey not in reached) or (childNode.cost < reached[stateKey]):
                reached[stateKey] = childNode.cost
                heapq.heappush(frontier, (problem.heuristic(childNode), childNode))

    return False


def aStar(problem: HeuristicProblem):
    frontier = []

    for node in problem.initialNodes:
        f = node.cost + problem.heuristic(node)  # f(n) = g(n) + h(n)
        heapq.heappush(frontier, (f, node))

    reached = {problem.hashableState(node): node.cost for node in problem.initialNodes}

    while frontier:
        _, currNode = heapq.heappop(frontier)

        if problem.isGoal(currNode):
            return True

        for child in problem.expand(currNode):
            stateKey = problem.hashableState(child)
            g = child.cost
            if stateKey not in reached or g < reached[stateKey]:
                reached[stateKey] = g
                f = g + problem.heuristic(child)
                heapq.heappush(frontier, (f, child))

    return False
