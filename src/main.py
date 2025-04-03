from searchAlgorithms import uninformedSearch as search
from problems.Resgate import Rescue, RescueState
from instances import instances


instance = instances[0]

park = instance["park"]
n = instance["N"]
time = instance["time"]
objective = instance["K"]
totalVictims = instance["W"]

gates = [(n // 2, n - 1), (n // 2, 0), (0, n // 2), (n - 1, n // 2)]

for gate in gates:
    initialState = RescueState(gate, False, time)
    rescue = Rescue(initialState, park, objective, totalVictims)

    if search.depthLimitedSearch(rescue, 100):
        rescue.printSolution()
    else:
        print("No solution was found")

# TODO:
# 1) search all the gates inside the problem
# 2) add table info in the problem class
# 3) time the algorithms
# 3) print the table
