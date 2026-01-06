with open("input.txt") as f:
    ranges_, ids_ = f.read().strip().split("\n\n")
    ranges = [tuple(map(int, range_.split("-"))) for range_ in ranges_.split()]
    ids = map(int, ids_.strip().split())

fresh = 0

for id_ in ids:
    for start, end in ranges:
        if start <= id_ <= end:
            fresh += 1
            break

print(f"{fresh=}")
