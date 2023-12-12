from itertools import combinations
from typing import NamedTuple

import numpy as np
from pandas import DataFrame

EMPTY = "."
GALAXY = "#"


class Point(NamedTuple):
    x: int
    y: int


def read_image(input_path: str) -> DataFrame:
    with open(input_path) as f:
        return DataFrame([list(line.strip()) for line in f])


class EmptySpace(NamedTuple):
    rows: list[int]
    cols: list[int]


def expand_point(point: Point, expansion: int, empty_space: EmptySpace) -> Point:
    x_shift = (expansion - 1) * len([row for row in empty_space.rows if point.x > row])
    y_shift = (expansion - 1) * len([col for col in empty_space.cols if point.y > col])
    return Point(point.x + x_shift, point.y + y_shift)


def sum_distances(image: DataFrame, empty_space: EmptySpace, expansion: int) -> int:
    points = (Point(x, y) for x, y in zip(*np.where(image == GALAXY)))
    points_x = map(lambda p: expand_point(p, expansion, empty_space), points)
    distances = (abs(a.x - b.x) + abs(a.y - b.y) for a, b in combinations(points_x, 2))
    return sum(distances)


if __name__ == "__main__":
    image = read_image("input.txt")

    empty_space = EmptySpace(
        rows=[i for i, row in image.iterrows() if all(pixel == EMPTY for pixel in row)],
        cols=[int(col) for col in image.columns if all(image[col] == EMPTY)],
    )

    part1_res = sum_distances(image, empty_space, expansion=2)
    print("(Part 1) Distances sum:", part1_res)

    part2_res = sum_distances(image, empty_space, expansion=1_000_000)
    print("(Part 2) Distances sum:", part2_res)
