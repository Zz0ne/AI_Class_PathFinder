from time import time
from threading import Thread
import csv

from searchAlgorithms import uninformedSearch as search
from problems.Resgate import Rescue
from instances import instances


def printAsciiTable(data, title=""):
    if not data:
        print("No data to display.")
        return

    headers = list(data[0].keys())
    col_widths = [
        max(len(str(row[h])) for row in data + [dict(zip(headers, headers))])
        for h in headers
    ]

    total_width = sum(col_widths) + len(col_widths) * 3 + 1

    if title:
        print(title.center(total_width, "="))

    header_row = (
        "|"
        + "|".join(f" {h.ljust(col_widths[i])} " for i, h in enumerate(headers))
        + "|"
    )
    separator = (
        "+" + "+".join("-" * (col_widths[i] + 2) for i in range(len(headers))) + "+"
    )

    print(separator)
    print(header_row)
    print(separator)

    for row in data:
        row_str = (
            "|"
            + "|".join(
                f" {str(row[h]).ljust(col_widths[i])} " for i, h in enumerate(headers)
            )
            + "|"
        )
        print(row_str)

    print(separator + "\n")


if __name__ == "__main__":

    table1 = []
    table2 = []

    algorithms = [
        {
            "name": "DepthFirstSearch",
            "function": search.depthFirstSearch,
            "args": [None],
            "table": [],
        },
        {
            "name": "BreadthFirstSearch",
            "function": search.breadthFirstSearch,
            "args": [None],
            "table": [],
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
        printAsciiTable(algorithm["table"], title=f" Results for {algorithm['name']} ")

    for algorithm in algorithms:
        filename = f"{algorithm['name']}_results.csv"

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=algorithm["table"][0].keys())

            writer.writeheader()
            writer.writerows(algorithm["table"])
