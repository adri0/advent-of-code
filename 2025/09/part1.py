from itertools import combinations

with open("input.txt") as f:
    coords = [tuple(map(int, line.split(","))) for line in f]

max_area = 0
for (x1, y1), (x2, y2) in combinations(coords, 2):
    area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
    if area > max_area:
        max_area = area

print(f"{max_area=}")
