from itertools import combinations
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def trace_outer_border(red_tiles: list[Point]) -> set[Point]:
    """
    Given a list of edges going clockwise forming a polygon,
    create a set of points forming the outer border of the polygon.
    """
    border = set()
    for i, p in enumerate(red_tiles):
        prev = red_tiles[i - 1]
        next = red_tiles[(i + 1) % len(red_tiles)]

        # right and up
        if prev.x < p.x and prev.y == p.y and next.x == p.x and next.y < p.y:
            for j in range(p.y - 1, next.y, -1):
                border.add(Point(p.x - 1, j))

        # up and right
        elif prev.x == p.x and prev.y > p.y and next.x > p.x and next.y == p.y:
            border.add(Point(p.x - 1, p.y))
            border.add(Point(p.x - 1, p.y - 1))
            for i in range(p.x, next.x):
                border.add(Point(i, p.y - 1))

        # right and down
        elif prev.x < p.x and prev.y == p.y and next.x == p.x and next.y > p.y:
            border.add(Point(p.x, p.y - 1))
            border.add(Point(p.x + 1, p.y - 1))
            for j in range(p.y, next.y):
                border.add(Point(p.x + 1, j))

        # down and right
        elif prev.x == p.x and prev.y < p.y and next.x > p.x and next.y == p.y:
            for i in range(p.x + 1, next.x):
                border.add(Point(i, p.y - 1))

        # left and down
        elif prev.x > p.x and prev.y == p.y and next.x == p.x and next.y > p.y:
            for j in range(p.y + 1, next.y):
                border.add(Point(p.x + 1, j))

        # down and left
        elif prev.x == p.x and prev.y < p.y and next.x < p.x and next.y == p.y:
            border.add(Point(p.x + 1, p.y))
            border.add(Point(p.x + 1, p.y + 1))
            for i in range(next.x + 1, p.x):
                border.add(Point(i, p.y + 1))

        # up and left
        elif prev.x == p.x and prev.y > p.y and next.x < p.x and next.y == p.y:
            for i in range(next.x + 1, p.x - 1):
                border.add(Point(i, p.y + 1))

        # left and up
        elif prev.x > p.x and prev.y == p.y and next.x == p.x and next.y < p.y:
            border.add(Point(p.x, p.y + 1))
            border.add(Point(p.x - 1, p.y + 1))
            for j in range(next.y + 1, p.x + 1):
                border.add(Point(p.x - 1, j))

        else:
            raise ValueError("Something is wrong")

    return border


def any_point_in_rectangle(rectangle: tuple[Point, Point], points: set[Point]) -> bool:
    """Check if a rectangle defined by two points contains any of the points in a set."""
    p1, p2 = rectangle
    for p in points:
        (min_x, max_x) = sorted([p1.x, p2.x])
        (min_y, max_y) = sorted([p1.y, p2.y])
        if (min_x <= p.x <= max_x) and (min_y <= p.y <= max_y):
            return True
    return False


if __name__ == "__main__":
    with open("input.txt") as f:
        red_tiles = [Point(*map(int, line.split(","))) for line in f]

    outer_border = trace_outer_border(red_tiles)

    max_area = 0
    for rectangle in combinations(red_tiles, 2):
        p1, p2 = rectangle
        area = (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)
        if area > max_area and not any_point_in_rectangle(rectangle, outer_border):
            max_area = area

    print(f"{max_area=}")
