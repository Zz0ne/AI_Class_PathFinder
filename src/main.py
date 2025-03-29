from searchAlgorithms import uninformedSearch as search
from problems.Puzzle8 import Puzzle8

startState = [3, 6, 1, 2, 8, 0, 4, 7, 5]
goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]

puzzle8 = Puzzle8(startState, goalState)

if search.breadthFirstSearch(puzzle8):
    currNode = puzzle8.goalNode
    while currNode:
        print(currNode.state)
        currNode = currNode.parent
else:
    print("No solution was found")
