from time import time
from threading import Thread
import csv

from prints import printPark, printTable
from searchAlgorithms import uninformedSearch as search
from problems.Resgate import Rescue
from instances import instances


if __name__ == "__main__":

    table1 = []
    table2 = []

    algorithms = [
        {
            "name": "DepthFirstSearch",
            "function": search.depthFirstSearch,
            "args": [None],
            "table": [],
            "resultData": [],
        },
        {
            "name": "BreadthFirstSearch",
            "function": search.breadthFirstSearch,
            "args": [None],
            "table": [],
            "resultData": [],
        },
    ]

    for num, instance in enumerate(instances):
        park = instance["park"]
        n = instance["N"]
        timeLeft = instance["time"]
        objective = instance["K"]
        totalVictims = instance["W"]

        algorithms[0]["args"][0] = Rescue(park, n, objective, totalVictims, timeLeft)
        algorithms[1]["args"][0] = Rescue(park, n, objective, totalVictims, timeLeft)

        for algorithm in algorithms:

            elapsedTime = [0.0]

            def runSearch():
                startTime = time()
                algorithm["function"](*algorithm["args"])
                endTime = time()
                elapsedTime[0] = endTime - startTime

            t = Thread(target=runSearch, daemon=True)

            t.start()
            t.join(timeout=10)

            resultData = algorithm["args"][0].getResultData()
            algorithm["resultData"].append(resultData)

            if resultData:
                algorithm["table"].append(
                    {
                        "Instancia": num + 1,
                        "Custo": resultData[0],
                        "Expansões": resultData[1],
                        "Gerações": resultData[2],
                        "Tempo": f"{elapsedTime[0]:.2}",
                    }
                )
            else:
                algorithm["table"].append(
                    {
                        "Instancia": num + 1,
                        "Custo": "",
                        "Expansões": "",
                        "Gerações": "",
                        "Tempo": "",
                    }
                )

    for algorithm in algorithms:
        pass
        # printTable(algorithm["table"], title=f" Results for {algorithm['name']} ")

    for i, instance in enumerate(instances):
        for algorithm in algorithms:
            print(algorithm["name"])

            cost = algorithm["table"][i]["Custo"]
            resultData = algorithm["resultData"][i]
            rescued = resultData[3]
            time = resultData[4]

            part2Path = algorithm["args"][0].getPath()
            part2Size = len(part2Path)
            part1Size = part2Size // 2
            part1Path = part2Path[:part1Size]

            print(f"Parte 1, passos {part1Size}:")
            printPark(part1Path, instance["park"], instance["N"])

            print(f"Parte 2, passos {part2Size}:")
            printPark(part2Path, instance["park"], instance["N"])
            print(f"Tempo: {time} ({rescued}/{instance['W']}), custo {resultData[0]}")
            print()

    # for algorithm in algorithms:
    #     filename = f"{algorithm['name']}_results.csv"
    #
    #     with open(filename, mode="w", newline="", encoding="utf-8") as file:
    #         writer = csv.DictWriter(file, fieldnames=algorithm["table"][0].keys())
    #
    #         writer.writeheader()
    #         writer.writerows(algorithm["table"])
