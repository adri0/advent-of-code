from typing import Iterator, NamedTuple

Map = list[list[str]]


class Pos(NamedTuple):
    x: int
    y: int


def read_input(path: str) -> Map:
    with open(path, "r") as f:
        return [list(line.strip()) for line in f]


def traverse(map_: Map) -> Iterator[Pos]:
    for j in range(len(map_)):
        for i in range(len(map_[0])):
            yield Pos(i, j)


def find_cursor(map_: Map) -> Pos:
    for pos in traverse(map_):
        if map_[pos.y][pos.x] == "^":
            return pos
    raise ValueError("Not found")


def within_boundaries(pos: Pos, map_: Map) -> bool:
    return 0 <= pos.x < len(map_[0]) and 0 <= pos.y < len(map_)


def print_map(map_: Map) -> None:
    for pos in traverse(map_):
        end = "" if pos.x < len(map_) - 1 else "\n"
        print(map_[pos.y][pos.x], end=end)
    print("------------")


def do_step(pos: Pos, map_: Map) -> Pos:
    # print_map(map_)
    dir = map_[pos.y][pos.x]

    if dir == "^":
        step_x, step_y = 0, -1
    elif dir == ">":
        step_x, step_y = +1, 0
    elif dir == "v":
        step_x, step_y = 0, 1
    elif dir == "<":
        step_x, step_y = -1, 0
    else:
        raise ValueError("Cur pos is not the cursor!")

    next_pos = Pos(pos.x + step_x, pos.y + step_y)
    if not within_boundaries(next_pos, map_):
        return next_pos

    if map_[next_pos.y][next_pos.x] == "#":
        turn_right(pos, map_)
        return do_step(pos, map_)

    map_[next_pos.y][next_pos.x] = dir
    map_[pos.y][pos.x] = "."

    return next_pos


def turn_right(pos: Pos, map_: Map) -> None:
    cur_dir = map_[pos.y][pos.x]
    dirs = ("^", ">", "v", "<")
    map_[pos.y][pos.x] = dirs[(dirs.index(cur_dir) + 1) % len(dirs)]


def part1(map_: Map) -> int:
    pos = find_cursor(map_)
    visited = set()
    while within_boundaries(pos, map_):
        visited.add(pos)
        pos = do_step(pos, map_)
    return len(visited)


if __name__ == "__main__":
    map_ = read_input("06/sample_input.txt")
    res1 = part1(map_)
    print(f"(part1) result: {res1}")
