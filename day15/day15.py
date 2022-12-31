from functools import partial, reduce
from operator import add
from typing import NamedTuple, Optional

from tqdm import tqdm


class Point(NamedTuple):
    x: int
    y: int


class Sensor(NamedTuple):
    pos: Point
    beacon: Point
    reach: int


class Interval(NamedTuple):
    """Closed interval"""

    left: int
    right: int


def distance(a: Point, b: Point) -> int:
    return abs(b.x - a.x) + abs(b.y - a.y)


def parse_sensor_data(input_path: str) -> list[Sensor]:
    sensors = []
    for line in open(input_path):
        part1, part2 = line.strip().split(":")
        x_sen = int(part1[part1.find("x=") + 2 : part1.find(",")])
        y_sen = int(part1[part1.find("y=") + 2 :])
        x_bea = int(part2[part2.find("x=") + 2 : part2.find(",")])
        y_bea = int(part2[part2.find("y=") + 2 :])
        sensor_pos = Point(x_sen, y_sen)
        beacon = Point(x_bea, y_bea)
        sensor = Sensor(
            pos=sensor_pos, beacon=beacon, reach=distance(sensor_pos, beacon)
        )
        sensors.append(sensor)
    return sensors


def row_coverage_by_sensor(y_row: int, sensor: Sensor) -> Optional[Interval]:
    mid_point = Point(sensor.pos.x, y_row)
    dist_mid_point = distance(sensor.pos, mid_point)
    if dist_mid_point > sensor.reach:
        return None
    row_reach = sensor.reach - dist_mid_point
    return Interval(left=sensor.pos.x - row_reach, right=sensor.pos.x + row_reach)


def row_coverage_by_sensor_points(y_row: int, sensor: Sensor) -> set[Point]:
    match row_coverage_by_sensor(y_row, sensor):
        case Interval(left, right):
            return {Point(x, y=y_row) for x in range(left, right + 1)}
        case None:
            return set()


def points_covered_in_row(y_row: int, sensors: list[Sensor]) -> set[Point]:
    return reduce(
        set.union, map(partial(row_coverage_by_sensor_points, y_row), tqdm(sensors))
    )


def part1(sensors: list[Sensor], y_row: int) -> None:
    cov_count_row = len(points_covered_in_row(y_row, sensors))
    count_not_beacon = cov_count_row - len(
        set(
            filter(
                lambda beacon: beacon.y == y_row,
                map(lambda sensor: sensor.beacon, sensors),
            )
        )
    )
    print(f"Number of pos beacon can't be in in row {y_row}:", count_not_beacon)


def subtract_interval(a: Interval, b: Interval) -> list[Interval]:
    """
    Subtract from interval a all positions covered by interval b
    Result a list of intervals corresponding to remaining positions.
    """
    if b.left > a.right or b.right < a.left:  # [..b..].[..a..]. -> .......[..a..].
        return [a]
    if b.left <= a.left and b.right >= a.right:  # [..b...[.a..]..] -> ...............
        return []
    if b.left > a.left and b.right < a.right:  # [..a...[.b..]..] -> [..a..].....[a]
        return [Interval(a.left, b.left - 1), Interval(b.right + 1, a.right)]
    if b.left <= a.left:  # [..b..]...
        return [Interval(b.right + 1, a.right)]  # ...[..a..] -> .........[a]
    if b.right >= a.right:
        return [Interval(a.left, b.left - 1)]
    raise Exception(f"Missed dealing with case: {a} - {b}")


def find_uncovered_point(sensors: list[Sensor], boundary: int) -> Point:
    for y_row in tqdm(range(boundary)):
        covered_intervals = map(partial(row_coverage_by_sensor, y_row), sensors)
        covered_intervals = filter(None, covered_intervals)  # type: ignore

        uncovered = [Interval(left=0, right=boundary)]
        for covered_interval in covered_intervals:
            subtract_coverage = partial(subtract_interval, b=covered_interval)
            uncovered = reduce(add, map(subtract_coverage, uncovered), [])
            if len(uncovered) == 0:
                break
        else:
            interval = uncovered[0]
            assert len(uncovered) == 1
            assert interval.left == interval.right
            return Point(x=interval.left, y=y_row)

    raise Exception("No uncovered point found within boundary")


def part2(sensors: list[Sensor], boundary: int):
    point = find_uncovered_point(sensors, boundary)
    print("Point distress signal:", point)
    frequency = 4_000_000 * point.x + point.y
    print("Frequency distress signal:", frequency)


if __name__ == "__main__":
    # path_input, y_row, boundary = "sample_input.txt", 10, 20
    path_input, y_row, boundary = "input.txt", 2_000_000, 4_000_000
    sensors = parse_sensor_data(path_input)
    part1(sensors, y_row)
    part2(sensors, boundary)
