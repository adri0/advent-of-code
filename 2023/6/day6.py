import math
from functools import reduce
from operator import mul
from typing import NamedTuple


class Race(NamedTuple):
    time: int
    dist: int


def read_scores(input_path: str) -> list[Race]:
    with open(input_path) as f:
        lines = f.readlines()
    times, dists = (
        list(map(int, lines[i].split(":")[1].strip().split())) for i in (0, 1)
    )
    return list(Race(times[i], dists[i]) for i in range(len(times)))


# pt: press time
def calculate_better_pt(race: Race) -> list[int]:
    t = race.time
    d = race.dist
    min_better_pt, max_better_pt = (
        (t + sign * math.sqrt(t**2 - 4 * d)) / 2 for sign in (-1, 1)
    )
    better_pt = range(
        int(math.ceil(min_better_pt + 1e-10)),
        int(math.floor(max_better_pt - 1e-10)) + 1,
    )
    return list(better_pt)


def part1(races: list[Race]) -> None:
    result = reduce(mul, (len(calculate_better_pt(race)) for race in races))
    print("Product of number of better times per race:", result)


if __name__ == "__main__":
    races = read_scores("input.txt")
    part1(races)
