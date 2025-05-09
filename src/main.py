from problems.Puzzle8 import Puzzle8
from searchAlgorithms import informedSearch as search


initialState = [4, 1, 0, 2, 6, 3, 7, 5, 8]
goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]

p8 = Puzzle8(initialState, goalState)

if search.bestFirstSearch(p8):

    result = p8.goalNode
    steps = 0

    while result:
        print(result.state)
        result = result.parent
        steps += 1

    print(steps)
else:
    print("no solution")
