from itertools import combinations
from typing import Any, NamedTuple

import numpy as np
import pandas as pd

EMPTY = "."
GALAXY = "#"


class Point(NamedTuple):
    x: int
    y: int


def read_image(input_path: str) -> pd.DataFrame:
    with open(input_path) as f:
        lines = [list(line.strip()) for line in f.readlines()]
    return pd.DataFrame(lines)


def expand_empty(image: pd.DataFrame) -> pd.DataFrame:
    rows: list[Any] = []
    empty_row = [EMPTY] * len(image.columns)
    for _, row in image.copy().iterrows():
        rows.append(row.values)
        if all(pixel == EMPTY for pixel in row):
            for i in range(1_000_000):
                rows.append(empty_row)
    image = pd.DataFrame(rows)

    for col in image.copy().columns:
        if all(image.loc[:, col] == EMPTY):
            for i in range(1_000_000):
                image.insert(
                    loc=image.columns.get_loc(col), column=f"{col}'", value=EMPTY
                )
    image.columns = range(len(image.columns))

    return image


def part1(image: pd.DataFrame) -> None:
    points = list(Point(x, y) for x, y in zip(*np.where(image == GALAXY)))
    distances = [abs(a.x - b.x) + abs(a.y - b.y) for a, b in combinations(points, 2)]
    result = sum(distances)
    print("Sum of distance:", result)


if __name__ == "__main__":
    image = read_image("input.txt")
    image = expand_empty(image)
    print(image)
    part1(image)
