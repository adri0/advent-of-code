Point = tuple[int, int]


def parse_beacons_input(input_path) -> dict[Point, Point]:
    sensors_to_beacon = {}
    for line in open(input_path):
        part1, part2 = line.strip().split(":")
        x_s = int(part1[part1.find("x=")+2 : part1.find(",")])
        y_s = int(part1[part1.find("y=")+2 :])
        x_b = int(part2[part2.find("x=")+2 : part2.find(",")])
        y_b = int(part2[part2.find("y=")+2 :])
        sensors_to_beacon[(x_s, y_s)] = (x_b, y_b)
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


def is_covered(point, sensors_reach) -> bool:
    for sensor, reach in sensors_reach.items():
        if distance(sensor, point) <= reach:
            return True
    return False


def count_positions_no_beacon(row, sensors_reach, beacons):
    leftmost_pos = min(x_s - reach for (x_s, _), reach in sensors_reach.items())
    rightmost_pos = max(x_s + reach for (x_s, _), reach in sensors_reach.items())
    beacons_in_row = len(set(filter(lambda pos: pos[1] == row, beacons)))
    return sum(
        [
            is_covered((row, x), sensors_reach)
            for x in range(leftmost_pos, rightmost_pos + 1)
        ]
    ) - beacons_in_row


sensors_to_beacon = parse_beacons_input("sample_input.txt")
sensors_reach = get_sensors_reach(sensors_to_beacon)
print(
    count_positions_no_beacon(
        row=10,
        sensors_reach=sensors_reach,
        beacons=set(sensors_to_beacon.values())
    )
)
