from searchAlgorithms import uninformedSearch as search
from problems.Resgate import Rescue, RescueState
from instances import instances


# for instance in instances:
instance = instances[1]
park = instance["park"]
n = instance["N"]
time = instance["time"]
objective = instance["K"]
totalVictims = instance["W"]

rescue = Rescue(park, n, objective, totalVictims, time)

if search.depthLimitedSearch(rescue, 50):
    rescue.printSolution()
else:
    print("No solution was found")

    # print("------")
    #
    # if search.depthLimitedSearch(rescue, 100):
    #     rescue.printSolution()
    # else:
    #     print("No solution was found")

# TODO:
# 1) search all the gates inside the problem
# 2) add table info in the problem class
# 3) time the algorithms
# 3) print the table
