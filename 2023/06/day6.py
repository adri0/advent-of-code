import math
from typing import NamedTuple


class Race(NamedTuple):
    time: int
    dist: int


def read_races(input_path: str, as_one: bool = False) -> list[Race]:
    with open(input_path) as f:
        lines = f.readlines()
    split_or_join = lambda s: s.split() if not as_one else [s.replace(" ", "")]
    times, dists = (
        map(int, split_or_join(lines[line_number].split(":")[1].strip()))
        for line_number in (0, 1)
    )
    return [Race(time, dist) for time, dist in zip(times, dists)]


def calculate_better_pt(race: Race) -> range:
    """
    distance: D
    total race time: t
    pressing time: pt
    velocity: v

    D = v * t
    v = 1 * pt
    =>
    D = (t - pt) * pt = t * pt - pt^2

    To find pt that beats a distance d:
    D > d
    t * pt - pt^2 > d

    Solve: pt^2 - t * pt + d < 0
    """
    t = race.time
    d = race.dist
    pt_low, pt_high = ((t + sign * math.sqrt(t**2 - 4 * d)) / 2 for sign in (-1, 1))
    pt = range(
        int(math.ceil(pt_low + 1e-10)),
        int(math.floor(pt_high - 1e-10)) + 1,
    )
    return pt


def part1(input_path: str) -> None:
    races = read_races(input_path)
    result = math.prod(len(calculate_better_pt(race)) for race in races)
    print("Result part 1:", result)


def part2(input_path: str) -> None:
    race, *_ = read_races(input_path, as_one=True)
    result = len(calculate_better_pt(race))
    print("Result part 2:", result)


if __name__ == "__main__":
    input_path = "input.txt"
    part1(input_path)
    part2(input_path)
