from typing import Iterable, NamedTuple


class DigPlanRow(NamedTuple):
    direction: str
    steps: int
    colour: str


class Point(NamedTuple):
    x: int
    y: int


def read_dig_plan(input_path: str) -> list[DigPlanRow]:
    with open(input_path) as f:
        return [
            DigPlanRow(
                direction=line[0],
                steps=int(line[1 : line.find(" ", 2)]),
                colour=line[line.find("#") + 1 : line.find(")")],
            )
            for line in f
        ]


def follow_dig_plan(dig_plan: Iterable[DigPlanRow]) -> set[Point]:
    cur_point = Point(0, 0)
    path = {cur_point}
    for row in dig_plan:
        match row.direction:
            case "R":
                segment = [
                    Point(cur_point.x, cur_point.y + i) for i in range(1, row.steps + 1)
                ]
            case "L":
                segment = [
                    Point(cur_point.x, cur_point.y - i) for i in range(1, row.steps + 1)
                ]
            case "U":
                segment = [
                    Point(cur_point.x - i, cur_point.y) for i in range(1, row.steps + 1)
                ]
            case "D":
                segment = [
                    Point(cur_point.x + i, cur_point.y) for i in range(1, row.steps + 1)
                ]
        path.update(segment)
        cur_point = segment[-1]
    return path


def display_points(points: Iterable[Point]) -> None:
    x_min = min(map(lambda p: p.x, points))
    x_max = max(map(lambda p: p.x, points))
    y_min = min(map(lambda p: p.y, points))
    y_max = max(map(lambda p: p.y, points))
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            if Point(i, j) in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


def update_dig_plan_row(row: DigPlanRow) -> DigPlanRow:
    return DigPlanRow(
        direction="RDLU"[int(row.colour[-1])], steps=int(row.colour[:-1], 16), colour=""
    )


def is_turn(i: int, dig_plan: list[DigPlanRow]) -> bool:
    return i + 1 == len(dig_plan) or (
        dig_plan[i - 1].direction == "D"
        and dig_plan[i + 1].direction == "U"
        or dig_plan[i - 1].direction == "U"
        and dig_plan[i + 1].direction == "D"
    )


def area_from_dig_plan(dig_plan: list[DigPlanRow]) -> int:
    cur_point = Point(0, 3)
    area = 0
    for i, row in enumerate(dig_plan):
        match row.direction:
            case "R":
                next_point = Point(cur_point.x, cur_point.y + row.steps)
                if is_turn(i, dig_plan):
                    area += abs(cur_point.y - next_point.y) + 1
                elif dig_plan[i - 1].direction == "D":
                    area += max(next_point.y, cur_point.y) + 1
                elif dig_plan[i - 1].direction == "U":
                    area -= min(next_point.y, cur_point.y)
                else:
                    raise ValueError("Dont know vertical dir")
            case "L":
                next_point = Point(cur_point.x, cur_point.y - row.steps)
                if is_turn(i, dig_plan):
                    area += abs(cur_point.y - next_point.y) + 1
                elif dig_plan[i - 1].direction == "D":
                    area += max(next_point.y, cur_point.y) + 1
                elif dig_plan[i - 1].direction == "U":
                    area -= min(next_point.y, cur_point.y)
                else:
                    raise ValueError("Dont know vertical dir")
            case "U":
                next_point = Point(cur_point.x - row.steps, cur_point.y)
                area -= (abs(next_point.x - cur_point.x) - 1) * (next_point.y)
            case "D":
                next_point = Point(cur_point.x + row.steps, cur_point.y)
                area += (next_point.x - cur_point.x - 1) * (next_point.y + 1)
        cur_point = next_point

    return area


def part1(dig_plan: list[DigPlanRow]) -> None:
    vol = area_from_dig_plan(dig_plan)
    print("(Part 1) Volume:", vol)


def part2(dig_plan: Iterable[DigPlanRow]) -> None:
    dig_plan = list(map(update_dig_plan_row, dig_plan))
    area = area_from_dig_plan(dig_plan)
    print("(Part 2) Area:", area)


if __name__ == "__main__":
    dig_plan = read_dig_plan("input.txt")
    part1(dig_plan)
    part2(dig_plan)
