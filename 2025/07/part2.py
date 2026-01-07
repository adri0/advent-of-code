with open("input.txt") as f:
    # Read grid and replacing dots by zero
    grid: list[list[str | int]] = [
        [{".": 0}.get(char, char) for char in line] for line in f.read().strip().split()
    ]


for i in range(1, len(grid)):
    for j in range(len(grid[0])):
        current = grid[i][j]
        previous = grid[i - 1][j]
        if previous == "S":
            # keep number of timelines at position instead of "|"
            grid[i][j] = 1
        elif isinstance(previous, int):
            if current == "^":
                grid[i][j - 1] += previous
                grid[i][j + 1] += previous
            else:
                grid[i][j] += previous

timelines = sum(x for x in grid[i] if isinstance(x, int))

print(f"{timelines=}")
