with open("input.txt") as f:
    # Add an extra border of dots around the original grid to avoid border conditions
    grid = ["." + line.strip() + "." for line in f]
    extra_row = ["." * len(grid[0])]
    grid = extra_row + grid + extra_row

accessible_rolls = 0
adjacent_steps = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] != "@":
            continue

        adjacent_rolls = 0
        for si, sj in adjacent_steps:
            if grid[i + si][j + sj] == "@":
                adjacent_rolls += 1

        if adjacent_rolls < 4:
            accessible_rolls += 1

print(f"{accessible_rolls=}")
