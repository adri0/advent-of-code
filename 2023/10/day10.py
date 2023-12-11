from typing import NamedTuple, Optional

START = "S"


class Point(NamedTuple):
    x: int
    y: int


def read_maze(input_path: str) -> tuple[list[str], Point]:
    maze = []
    start = None
    with open(input_path) as f:
        for j, line in enumerate(f):
            maze.append(line.strip())
            if not start and START in line:
                start = Point(line.index(START), j)
    if not start:
        raise ValueError("Cannot find start")
    return (maze, start)


VISITED: list[Point] = []


def show_maze(maze: list[str], visited: Optional[list[Point]] = None) -> None:
    for j in range(len(maze)):
        for i in range(len(maze[j])):
            if visited and Point(i, j) in visited:
                print(
                    ("\033[4m" if Point(i, j) == visited[-1] else "")
                    + f"\033[92m\033[1m{maze[j][i]}\033[0m",
                    end="",
                )
            else:
                print(maze[j][i], end="")
        print()


def find_next_point(prev: Point, cur: Point, maze: list[str]) -> Point:
    pipe = maze[cur.y][cur.x]
    VISITED.append(cur)
    if pipe == "|":  # ok
        y_next = cur.y + (1 if prev.y < cur.y else -1)
        return Point(cur.x, y_next)
    elif pipe == "-":
        x_next = cur.x + (1 if prev.x < cur.x else -1)
        return Point(x_next, cur.y)
    elif pipe == "F":
        shift = +1 if prev.x == cur.x else -1
        return Point(prev.x + shift, prev.y - shift)
    elif pipe == "7":
        shift = +1 if prev.y == cur.y else -1
        return Point(prev.x + shift, prev.y + shift)
    elif pipe == "J":
        shift = +1 if prev.y == cur.y else -1
        return Point(prev.x + shift, prev.y - shift)
    elif pipe == "L":
        shift = +1 if prev.y == cur.y else -1
        return Point(prev.x - shift, prev.y - shift)
    else:
        raise ValueError("Something's not right")


def find_valid_next(cur: Point, maze: list[str]) -> Point:
    if maze[cur.y][cur.x - 1] in ("-", "L", "F"):
        return Point(cur.x - 1, cur.y)
    elif maze[cur.y - 1][cur.x] in ("|", "F", "7"):
        return Point(cur.x, cur.y - 1)
    elif maze[cur.y][cur.x + 1] in ("-", "7", "J"):
        return Point(cur.x + 1, cur.y)
    elif maze[cur.y + 1][cur.x] in ("|", "J", "L"):
        return Point(cur.x, cur.y + 1)
    else:
        raise ValueError("Cannot find valid previous")


def part1(maze: list[str], start: Point) -> None:
    n = 1
    current = find_valid_next(start, maze)
    prev = start
    while current != start:
        prev, current = current, find_next_point(prev, current, maze)
        n += 1
    print("Steps to cycle:", n)
    print("Halfway:", n // 2)


if __name__ == "__main__":
    maze, start = read_maze("input.txt")
    show_maze(maze)
    part1(maze, start)
