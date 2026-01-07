with open("input.txt") as f:
    # Read grid replacing dots by zero and S by 1
    grid: list[list[str | int]] = [
        [{".": 0, "S": 1}.get(char, char) for char in line]
        for line in f.read().strip().split()
    ]

for i in range(1, len(grid)):
    for j in range(len(grid[0])):
        if (previous := grid[i - 1][j]) != "^":
            if grid[i][j] == "^":
                grid[i][j - 1] += previous
                grid[i][j + 1] += previous
            else:
                grid[i][j] += previous

timelines = sum(v for v in grid[i] if isinstance(v, int))

print(f"{timelines=}")
