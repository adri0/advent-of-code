from functools import reduce, partial
from dataclasses import dataclass
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Sensor:
    pos: Point
    beacon: Point
    reach: int


def distance(a: Point, b: Point) -> int:
    return abs(b.x - a.x) + abs(b.y - a.y)


def parse_sensor_data(input_path: str) -> list[Sensor]:
    sensors = []
    for line in open(input_path):
        part1, part2 = line.strip().split(":")
        x_sen = int(part1[part1.find("x=")+2 : part1.find(",")])
        y_sen = int(part1[part1.find("y=")+2 :])
        x_bea = int(part2[part2.find("x=")+2 : part2.find(",")])
        y_bea = int(part2[part2.find("y=")+2 :])
        sensor_pos = Point(x_sen, y_sen)
        beacon = Point(x_bea, y_bea)
        sensor = Sensor(
            pos=sensor_pos, 
            beacon=beacon, 
            reach=distance(sensor_pos, beacon)
        )
        sensors.append(sensor)      
    return sensors


def row_coverage_by_sensor(y_row: int, sensor: Sensor) -> set[Point]:
    mid_point = Point(sensor.pos.x, y_row)
    dist_mid_point = distance(sensor.pos, mid_point)
    if dist_mid_point > sensor.reach:
        return set()
    row_reach = sensor.reach - dist_mid_point 
    return {
        Point(x, y_row)
        for x in range(sensor.pos.x - row_reach, sensor.pos.x + row_reach + 1)
    }


def count_points_covered_in_row(y_row: int, sensors: list[Sensor]) -> int:
    return len(
        reduce(
            lambda set1, set2: set1.union(set2),
            map(partial(row_coverage_by_sensor, y_row), sensors)
        )
    )


def part1(sensors: list[Sensor], y_row: int) -> None:
    cov_count_row = count_points_covered_in_row(y_row, sensors)
    count_not_beacon = cov_count_row - len(
        set(
            filter(
                lambda beacon: beacon.y == y_row,
                map(lambda sensor: sensor.beacon, sensors)
            )
        )
    )
    print(f"Number of pos beacon can't be in in row {y_row}:", count_not_beacon)


if __name__ == "__main__":
    sensors = parse_sensor_data("input.txt")
    part1(sensors, y_row=2_000_000)
