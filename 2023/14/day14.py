import re
from collections import defaultdict
from enum import Enum


def read_platform(input_path: str) -> tuple[str, ...]:
    with open(input_path) as f:
        return tuple(line.strip() for line in f)


def load_at_north_beam(platform: tuple[str, ...]) -> int:
    return sum(
        sum(len(platform) - i for char in row if char == "O")
        for i, row in enumerate(platform)
    )


class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


def part1(platform: tuple[str, ...]) -> None:
    platform = tilt_platform(platform, Direction.NORTH)
    print("(Part 1) Load north beam:", load_at_north_beam(platform))


MIN_OFFSET = 100


def tilt_row(row: str, left: bool = False) -> str:
    portions = []
    start = 0
    for match in re.finditer("#|$", row):
        portion = row[start : match.start()]
        n_round_rocks = sum(1 for char in portion if char == "O")
        n_empty = len(portion) - n_round_rocks
        if left:
            new_portion = "O" * n_round_rocks + "." * n_empty
        else:
            new_portion = "." * n_empty + "O" * n_round_rocks
        portions.append(new_portion)
        start = match.end()
    return "#".join(portions)


def tilt_platform(platform: tuple[str, ...], direction: Direction) -> tuple[str, ...]:
    match direction:
        case Direction.EAST:
            return tuple(map(tilt_row, platform))
        case Direction.WEST:
            return tuple(tilt_row(row, left=True) for row in platform)
        case Direction.NORTH:
            return transpose(
                tuple(tilt_row(row, left=True) for row in transpose(platform))
            )
        case Direction.SOUTH:
            return transpose(tuple(tilt_row(row) for row in transpose(platform)))


def transpose(platform: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        "".join(platform[col][row] for col in range(len(platform[0])))
        for row in range(len(platform))
    )


def part2(platform: tuple[str, ...]) -> None:
    platform_hash: dict[int, int] = defaultdict(int)

    for i in range(1_000_000_000):
        for direction in Direction:
            platform = tilt_platform(platform, direction)
        platform_hash[hash(platform)] += 1

        if len(platform_hash) + MIN_OFFSET < i:  # Detect a cycle
            offset = sum(1 for count in platform_hash.values() if count == 1)
            period = len(platform_hash) - offset
            if (1_000_000_000 - offset) % period == (i + 1 - offset) % period:
                break

    print("(Part 2) Load north beam:", load_at_north_beam(platform))


if __name__ == "__main__":
    platform = read_platform("input.txt")
    part1(platform)
    part2(platform)
