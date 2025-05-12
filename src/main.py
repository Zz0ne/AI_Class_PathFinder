from problems.Puzzle8 import Puzzle8
from searchAlgorithms import informedSearch as search


initialState = [8, 1, 6, 2, 3, 0, 7, 5, 4]
goalState = [1, 2, 3, 4, 5, 6, 7, 8, 0]

p8 = Puzzle8(initialState, goalState)

if search.bestFirstSearch(p8):

    result = p8.goalNode
    steps = 0

    while result:
        for i, tile in enumerate(result.state):
            print(tile, end=" ")
            if (i + 1) % 3 == 0:
                print()
        print()

        result = result.parent
        steps += 1

    print(steps)
else:
    print("no solution")
