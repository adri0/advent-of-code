from functools import reduce
from dataclasses import dataclass

Point = tuple[int, int]


@dataclass
class Sensor:
    pos: Point
    beacon: Point
    reach: int


def parse_beacons_input(input_path) -> dict[Point, Point]:
    sensors_to_beacon = {}
    for line in open(input_path):
        part1, part2 = line.strip().split(":")
        x_s = int(part1[part1.find("x=")+2 : part1.find(",")])
        y_s = int(part1[part1.find("y=")+2 :])
        x_b = int(part2[part2.find("x=")+2 : part2.find(",")])
        y_b = int(part2[part2.find("y=")+2 :])
        sensor = (x_s, y_s)
        beacon = (x_b, y_b)
        sensors_to_beacon[sensor] = beacon
    return sensors_to_beacon


def distance(a: Point, b: Point) -> int:
    x_a, y_a = a
    x_b, y_b = b
    return abs(x_b - x_a) + abs(y_b - y_a)


def get_sensors_reach(sensors_to_beacon: dict[Point, Point]) -> dict[Point, int]:
    return {
        sensor: distance(sensor, beacon) 
        for sensor, beacon in sensors_to_beacon.items()
    }


def coverage_in_row_by_sensor(y_row: int, sensor: Point, reach: int) -> set[Point]:
    x_sensor = sensor[0]
    mid_point = (x_sensor, y_row)
    dist_mid_point = distance(sensor, mid_point)
    if dist_mid_point > reach:
        return set()
    row_reach = reach - dist_mid_point 
    return {
        (x, y_row) 
        for x in range(x_sensor - row_reach, x_sensor + row_reach + 1)
    }


def count_points_covered_in_row(y_row, sensors_reach):
    return len(
        reduce(
            lambda set1, set2: set1.union(set2), 
            (
                coverage_in_row_by_sensor(y_row, sensor, reach) 
                for sensor, reach in sensors_reach.items()
            )
        )
    )


if __name__ == "__main__":
    sensors_to_beacon = parse_beacons_input("input.txt")
    sensors_reach = get_sensors_reach(sensors_to_beacon)
    y_row = 2000000
    # y_row = 10
    cov_count_row = count_points_covered_in_row(
        y_row=y_row, 
        sensors_reach=sensors_reach
    )
    count_occupied = cov_count_row - len(
        list(
            filter(
                lambda beacon: beacon[0] == y_row, 
                set(sensors_to_beacon.keys())
            )
        )
    )
    print(count_occupied)