
def segment_to_points(a, b):
    """ Create all points between a pair of points """
    ax, ay = a
    bx, by = b
    if ax == bx:
        return {(ax, y) for y in range(min(ay, by), max(ay, by) + 1)}
    elif ay == by:
        return {(x, ay) for x in range(min(ax, bx), max(ax, bx) + 1)}
    else:
        raise ValueError(f"a and b must be aligned in one of the axis: {a}, {b}")


def parse_cave_canvas(path):
    rock_points = set()
    for line in open(path):
        rock_segments = list(map(
            lambda node: tuple(map(int, node.split(","))), 
            line.strip().split(" -> ")
        ))
        for i in range(len(rock_segments) - 1):
            rock_points.update(segment_to_points(*rock_segments[i : i+2]))
    max_y = max([j for _, j in rock_points])
    return [
        [
            "#" if (x, y) in rock_points or y == max_y + 2 else "."
            for x in range(max([i for i, _ in rock_points]) + 1000) 
        ]
        for y in range(max_y + 2 + 1)
    ]


def print_cave(cave, x_start=490):
    for j in range(len(cave)):
        for i in range(x_start, len(cave[0])):
            print(cave[j][i], end="")
        print()


def drop_sand_grain(cave, initial_pos=(500,0)):
    i = initial_pos[0]
    for j in range(initial_pos[1], len(cave)):
        if cave[j][i] in ("#", "o"):
            if cave[j][i-1] == ".":
                return drop_sand_grain(cave, (i-1, j))
            elif cave[j][i+1] == ".":
                return drop_sand_grain(cave, (i+1, j))
            else:
                cave[j-1][i] = "o"
                return True
    return False


cave = parse_cave_canvas("input.txt")

grains = 0
while cave[0][500] == "." and drop_sand_grain(cave):
    grains += 1

print_cave(cave, x_start=455)

print("Grains:", grains)