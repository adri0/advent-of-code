LETTER_CODES = "SabcdefghijklmnopqrstuvwxyzE"


def load_map(path):
    """ Load map from input and convert to number codes """
    return [list(map(LETTER_CODES.find, line.strip())) for line in open(path)]


def find_start_end(map_ap):
    for j in range(len(map_ap)):
        for i in range(len(map_ap[0])):
            if map_ap[j][i] == 0:
                start = (i, j)
            if map_ap[j][i] == len(LETTER_CODES) - 1:
                end = (i, j)
    return start, end


def walk_next(map_ap, current_pos, visited, end):
    """ Walk to the next position """
    options = walk_options(map_ap, current_pos, visited)
    if not options:
        visualize(map_ap, current_pos, visited, milestones=[])
        raise Exception(f"Dead end at {current_pos}")
    return pick_next_pos(map_ap, options, end)


def distance(a, b):
    """ Manhattan """
    x_a, y_a = a
    x_b, y_b = b
    return abs(y_b - y_a) + abs(x_b - x_a)


def height_diff(map_ap, a, b):
    (x_a, y_a), (x_b, y_b) = a, b
    return map_ap[y_b][x_b] - map_ap[y_a][x_a]


def pick_next_pos(map_ap, walk_options, end):
    return sorted(
        walk_options,
        key=lambda option: distance(option, end) - 10 * height_diff(map_ap, end, option)
    )[0]


def walk_options(map_ap, current_pos, visited):
    """ Generate next walk options from the current position """
    x_cur, y_cur = current_pos
    height_cur = map_ap[y_cur][x_cur]
    adjencies = [
        (x_cur - 1, y_cur),
        (x_cur + 1, y_cur),
        (x_cur, y_cur - 1),
        (x_cur, y_cur + 1)
    ]
    options = []
    for i, j in adjencies:
        if (
            (i, j) in visited
            or i < 0 or j < 0 
            or i >= len(map_ap[0]) 
            or j >= len(map_ap)
        ):
            continue
        if map_ap[j][i] in (height_cur, height_cur - 1):
            options.append((i, j))
    return options


def visualize(map_ap, current_pos, visited, milestones):
    for j in range(len(map_ap)):
        for i in range(len(map_ap[0])):
            if (i, j) == current_pos:
                print("@", end="")
            elif (i, j) in visited:
                print(".", end="")
            elif (i, j) in milestones:
                print(LETTER_CODES[map_ap[j][i]].upper(), end="")
            else:
                print(LETTER_CODES[map_ap[j][i]], end="")
        print()
    print()

map_ap = load_map("input.txt")
start, end = find_start_end(map_ap)

# # Going from end to start instead
current_pos = end
end = start

steps = 0
visited = set([current_pos])
milestones = [(145, 23), (152, 26), (155, 15), (142, 29), end]
for milestone in milestones:
    while current_pos != milestone:
        current_pos = walk_next(map_ap, current_pos, visited, milestone)
        visited.add(current_pos)
        steps += 1

print("Final destination reached! Steps:", steps)
