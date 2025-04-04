from searchAlgorithms import uninformedSearch as search
from problems.Resgate import Rescue, RescueState
from instances import instances


for instance in instances:
    park = instance["park"]
    n = instance["N"]
    time = instance["time"]
    objective = instance["K"]
    totalVictims = instance["W"]

    rescue = Rescue(park, n, objective, totalVictims, time)

    # if search.iterativeDeepeningSearch(rescue, 100):
    # if search.depthLimitedSearch(rescue, 100):
    if search.breadthFirstSearch(rescue):
        # if search.uniformCostSearch(rescue):
        rescue.printSolution()
    else:
        print("No solution was found")

# TODO:
# 1) search all the gates inside the problem
# 2) add table info in the problem class
# 3) time the algorithms
# 3) print the table
