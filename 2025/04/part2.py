with open("input.txt") as f:
    # Add an extra border of dots around the original grid to avoid border conditions
    grid = [["."] + list(line.strip()) + ["."] for line in f]
    extra_row = [["."] * len(grid[0])]
    grid = extra_row + grid + extra_row

total_removed_rolls = 0
adjacent_steps = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
ongoing_removal = True

while ongoing_removal:
    removed_rolls = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "@":
                continue

            adjacent_rolls = 0
            for si, sj in adjacent_steps:
                if grid[i + si][j + sj] == "@":
                    adjacent_rolls += 1

            if adjacent_rolls < 4:
                grid[i][j] = "."
                removed_rolls += 1

    total_removed_rolls += removed_rolls
    ongoing_removal = removed_rolls > 0

print(f"{total_removed_rolls=}")
