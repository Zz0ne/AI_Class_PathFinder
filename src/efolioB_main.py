from time import time
from threading import Thread
import csv
from copy import deepcopy

from searchAlgorithms import informedSearch as search
from problems.ParkTour import ParkTour
from instancesEfolioB import instances
from prints import printTable, printPark

if __name__ == "__main__":

    table1 = []
    table2 = []

    algorithms = [
        {
            "name": "A*",
            "function": search.aStar,
            "args": [None],
            "table": [],
            "resultData": [],
            "path": [],
        },
        {
            "name": "BestFirstSearch",
            "function": search.bestFirstSearch,
            "args": [None],
            "table": [],
            "resultData": [],
            "path": [],
        },
    ]

    for num, instance in enumerate(instances):
        park = instance["park"]
        n = instance["N"]
        timeLeft = instance["time"]
        pointsOfInterestTotal = instance["K"]
        pointsOfInterestNum = instance["W"]

        algorithms[0]["args"][0] = ParkTour(
            park, n, pointsOfInterestNum, pointsOfInterestTotal, timeLeft
        )
        algorithms[1]["args"][0] = ParkTour(
            park, n, pointsOfInterestNum, pointsOfInterestTotal, timeLeft
        )

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

            if resultData:
                algorithm["resultData"].append(deepcopy(resultData))
                algorithm["path"].append(deepcopy(algorithm["args"][0].getPath()))

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
        printTable(algorithm["table"], title=f" Results for {algorithm['name']} ")

    # for algorithm in algorithms:
    #     filename = f"{algorithm['name']}_results.csv"
    #
    #     with open(filename, mode="w", newline="", encoding="utf-8") as file:
    #         writer = csv.DictWriter(file, fieldnames=algorithm["table"][0].keys())
    #
    #         writer.writeheader()
    #         writer.writerows(algorithm["table"])
    for i, instance in enumerate(instances):
        for algorithm in algorithms:
            print(algorithm["name"])

            try:
                resultData = algorithm["resultData"][i]
                cost = resultData[0]
                satisgaction = resultData[3]
                time = resultData[4]

                part2Path = algorithm["path"][i]
                part2Size = len(part2Path)
                part1Size = part2Size // 2
                part1Path = part2Path[:part1Size]
            except IndexError:
                continue

            # print(f"Instancia {i+1}")
            # print(f"Parte 1, passos {part1Size}:")
            # printPark(part1Path, instance["park"], instance["N"])

            print(f"Instancia {i+1}")
            print(f"Parte 2, passos {part2Size}:")
            printPark(part2Path, instance["park"], instance["N"])
            print(
                f"Tempo: {time} ({satisgaction}/{instance['K'] + instance['time']}), custo {cost}"
            )
            print()
