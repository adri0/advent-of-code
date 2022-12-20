Point = tuple[int, int]
Canvas = list[list[Point]]

AIR = "."
ROCK = "#"
SAND = "o"
HOLE_POS = (500, 0)


def segment_to_points(a: Point, b: Point) -> list[Point]:
    """ Create all points between a pair of points """
    x_a, y_a = a
    x_b, y_b = b
    if x_a == x_b:
        start, end = min(y_a, y_b), max(y_a, y_b)
        return [(x_a, y) for y in range(start, end + 1)]
    elif y_a == y_b:
        start, end = min(x_a, x_b), max(x_a, x_b)
        return [(x, y_a) for x in range(start, end + 1)]
    else:
        raise ValueError(f"a and b must be aligned in one of the axis: {a}, {b}")


def read_points_from_file(input_path: str) -> set[Point]:
    """ Load and parse input file into a set of points. """
    points = set()
    for line in open(input_path):
        segment_nodes = list(
            map(
                lambda node: tuple(map(int, node.split(","))), 
                line.strip().split(" -> ")
            )
        )
        for i in range(len(segment_nodes) - 1):
            points.update(set(segment_to_points(*segment_nodes[i:i+2])))
    return points


def draw_cave_canvas(rock_points: set[Point], draw_floor: bool) -> Canvas:
    """ 
    Given a set of rock points, create a canvas (matrix) adding enough room 
    for incoming sand.
    """
    max_x = max([x for x, _ in rock_points])
    max_y = max([y for _, y in rock_points])
    extra_room_x = 1000 if draw_floor else 0
    extra_room_y = 2 if draw_floor else 0
    return [
        [
            ROCK if (x, y) in rock_points or (draw_floor and y == max_y + 2)
            else AIR
            for x in range(max_x + extra_room_x + 1)
        ]
        for y in range(max_y + extra_room_y + 1)
    ]


def print_cave(cave: Canvas, x_start=490, x_end=None):
    for j in range(len(cave)):
        for i in range(x_start, x_end or len(cave[0])):
            print(cave[j][i], end="")
        print()


def drop_sand_grain(cave: Canvas, point: Point) -> bool:
    """ 
    Drop a grain of sand into the cave from a point. 
    Returns True if the sand remains inside the canvas. 
    """
    x, y = point
    for j in range(y, len(cave)):
        if cave[j][x] in (ROCK, SAND):
            if cave[j][x-1] == AIR:
                return drop_sand_grain(cave, (x-1, j))
            elif cave[j][x+1] == AIR:
                return drop_sand_grain(cave, (x+1, j))
            else:
                cave[j-1][x] = SAND
                return True
    return False


def count_dropped_sand(cave: Canvas) -> int:
    """ 
    Drop grain of sands from the hole until hole is covered 
    or a grain fall off the canvas. 
    """
    sand_grains = 0
    x_hole, y_hole = HOLE_POS
    while cave[y_hole][x_hole] == AIR and drop_sand_grain(cave, HOLE_POS):
        sand_grains += 1
    return sand_grains


def part1(rock_points):
    cave = draw_cave_canvas(rock_points, draw_floor=False)
    print("Grains (no floor):", count_dropped_sand(cave))


def part2(rock_points):
    cave = draw_cave_canvas(rock_points, draw_floor=True)
    print("Grains (yes floor):", count_dropped_sand(cave))


rock_points = read_points_from_file("input.txt")
part1(rock_points)
part2(rock_points)
