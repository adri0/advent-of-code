from dataclasses import dataclass
from functools import partial
from typing import Generator, Iterable, NamedTuple, Optional

Map = list[list[int]]


class Coord(NamedTuple):
    x: int
    y: int


LETTERS = "abcdefghijklmnopqrstuvwxyz"


def parse_map(input_path: str) -> tuple[Map, Coord, Coord]:
    """
    Load map from input file converting chars to elevation numbers
    and detect start and end coordinates.
    """
    map_mat: Map = []
    for j, line in enumerate(open(input_path)):
        row = []
        for i, char in enumerate(line.strip()):
            match char:
                case "S":
                    start = Coord(i, j)
                    char = "a"
                case "E":
                    end = Coord(i, j)
                    char = "z"
            row.append(LETTERS.index(char))
        map_mat.append(row)
    return map_mat, start, end


def within_boundaries(coord: Coord, map_mat: Map) -> bool:
    return (0 <= coord.x < len(map_mat[0])) and (0 <= coord.y < len(map_mat))


def get_valid_adjacents(
    map_mat: Map, cur: Coord, visited: set[Coord]
) -> Iterable[Coord]:
    """Get valid adjacent coordinates from a given coordinate"""
    cur_elevation = map_mat[cur.y][cur.x]

    def valid_adjacent(adj: Coord) -> bool:
        return (
            within_boundaries(adj, map_mat)
            and adj not in visited
            and map_mat[adj.y][adj.x] <= cur_elevation + 1
        )

    return filter(
        valid_adjacent,
        (
            Coord(cur.x, cur.y + 1),
            Coord(cur.x + 1, cur.y),
            Coord(cur.x, cur.y - 1),
            Coord(cur.x - 1, cur.y),
        ),
    )


def colorize(string: str) -> str:
    END = "\033[0m"
    COLOR = "\033[95m"
    BOLD = "\033[1m"
    return f"{BOLD}{COLOR}{string}{END}"


def traverse(map_mat: Map) -> Generator[tuple[Coord, int], None, None]:
    """Traverse the map and yield coordinates and elevation"""
    for j, row in enumerate(map_mat):
        for i, elev in enumerate(row):
            yield Coord(i, j), elev


def visualize(map_ap: Map, current_pos: Coord, visited: Iterable[Coord]) -> None:
    for coord, elev in traverse(map_mat):
        if coord == current_pos:
            print(colorize("*"), end="")
        elif coord in visited:
            print(colorize(LETTERS[elev]), end="")
        else:
            print(LETTERS[elev], end="")
        if coord.x == len(map_mat[0]) - 1:
            print()
    print()


@dataclass
class PathPos:
    """Represents a position in a path"""

    coord: Coord
    previous: Optional["PathPos"] = None


def breadth_first_search(map_mat: Map, start: Coord, end: Coord) -> Optional[PathPos]:
    """Breadth-first search to find the shortest path between start to end"""
    path_start = PathPos(start)
    queue: list[PathPos] = [path_start]
    visited: set[Coord] = set([path_start.coord])

    while len(queue) > 0:
        current = queue.pop(0)
        if current.coord == end:
            return current
        for adj_coord in get_valid_adjacents(map_mat, current.coord, visited):
            visited.add(adj_coord)
            next_pos = PathPos(adj_coord)
            next_pos.previous = current
            queue.append(next_pos)
    return None


def unroll_path(path_pos: PathPos) -> list[Coord]:
    """Get a list of coordinates in a path represented by its last position"""
    path = [path_pos.coord]
    while path_pos := path_pos.previous:  # type: ignore
        path.insert(0, path_pos.coord)
    return path


def part1(map_mat: list[list[int]], start: Coord, end: Coord) -> None:
    """Print minimum number of steps from start to end"""
    path_pos = breadth_first_search(map_mat, start, end)
    if not path_pos:
        raise Exception("No path found!")
    path = unroll_path(path_pos)
    visualize(map_mat, end, path)
    n_steps = len(path) - 1
    print(f"Minimum number of steps from start at {start}:", n_steps)


def part2(map_mat: list[list[int]], end: Coord) -> None:
    """Print minimum number of steps from any 'a' elevation to end"""
    elev_at_a = LETTERS.index("a")
    start = (coord for coord, elev in traverse(map_mat) if elev == elev_at_a)
    path_pos = map(partial(breadth_first_search, map_mat, end=end), start)
    path_pos_found = filter(None, path_pos)
    paths = map(unroll_path, path_pos_found)
    shortest_path = min(paths, key=len)
    visualize(map_mat, end, set(shortest_path))
    n_steps = len(shortest_path) - 1
    print("Minimum number of steps from any 'a' elevation:", n_steps)


if __name__ == "__main__":
    map_mat, start, end = parse_map("input.txt")
    part1(map_mat, start, end)
    part2(map_mat, end)
