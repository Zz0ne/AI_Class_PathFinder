from typing import List, Tuple


def printTable(data, title=""):
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


def printPark(path: List[Tuple[int, int]], park: List[List[int]], parkSize: int):
    middle = parkSize // 2

    visited = []
    southExit = (middle, parkSize)
    northExit = (middle, -1)
    westExit = (-1, middle)
    eastExit = (parkSize, middle)

    horizontalWall = ""

    if northExit == path[-1]:
        horizontalWall = "*" + "---" * (middle) + "|^|" + "---" * (middle) + "*"
    else:
        horizontalWall = "*" + "---" * (middle) + "| |" + "---" * (middle) + "*"

    print(horizontalWall)

    for rowNum, row in enumerate(park):

        rowStr = "|"

        if rowNum == middle:
            if westExit == path[-1]:
                rowStr = "<"
            else:
                rowStr = " "

        for tileNum, tile in enumerate(row):
            if (tileNum, rowNum) == path[-1]:
                if tile == 1:
                    rowStr += "[.]"
                elif tile == 2:
                    rowStr += "[:]"
                elif tile < 0:
                    rowStr += "[+]"
            elif path.count((tileNum, rowNum)) > 1:
                if tile == 1:
                    rowStr += "{.}"
                elif tile == 2:
                    rowStr += "{:}"
                elif tile < 0:
                    rowStr += "{+}"
            elif (tileNum, rowNum) in path:
                if tile == 1:
                    rowStr += "(.)"
                    visited.append((tileNum, rowNum))
                elif tile == 2:
                    rowStr += "(:)"
                    visited.append((tileNum, rowNum))
                elif tile < 0:
                    rowStr += "(+)"
                    visited.append((tileNum, rowNum))
            else:
                if tile == 10:
                    rowStr += " # "
                elif tile == 1:
                    rowStr += " . "
                elif tile == 2:
                    rowStr += " : "
                elif tile < 0:
                    rowStr += f" {abs(tile)} "

        if rowNum == middle:
            if eastExit == path[-1]:
                rowStr += ">"
            else:
                rowStr += " "
        else:
            rowStr += "|"
        print(rowStr)

    if southExit == path[-1]:
        horizontalWall = "*" + "---" * (middle) + "|v|" + "---" * (middle) + "*"
    else:
        horizontalWall = "*" + "---" * (middle) + "| |" + "---" * (middle) + "*"
    print(horizontalWall)
