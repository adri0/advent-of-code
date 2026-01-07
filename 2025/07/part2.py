with open("input.txt") as f:
    # Read grid replacing dots by zero
    grid: list[list[str | int]] = [
        [{".": 0}.get(char, char) for char in line] for line in f.read().strip().split()
    ]

for i in range(1, len(grid)):
    for j in range(len(grid[0])):
        match grid[i - 1][j]:
            case "S":
                grid[i][j] = 1  # number of timelines at position
            case int(n_timelines):
                if grid[i][j] == "^":
                    grid[i][j - 1] += n_timelines
                    grid[i][j + 1] += n_timelines
                else:
                    grid[i][j] += n_timelines

timelines = sum(v for v in grid[i] if isinstance(v, int))

print(f"{timelines=}")
