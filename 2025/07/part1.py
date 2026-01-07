with open("input.txt") as f:
    grid = [list(line) for line in f.read().strip().split()]

splits = 0

for i in range(1, len(grid)):
    for j in range(len(grid[0])):
        current = grid[i][j]
        previous = grid[i - 1][j]
        if previous in {"|", "S"}:
            if current == "^":
                splits += 1
                grid[i][j - 1] = "|"
                grid[i][j + 1] = "|"
            else:
                grid[i][j] = "|"

print(f"{splits=}")
