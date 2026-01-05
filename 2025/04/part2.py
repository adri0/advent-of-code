from typing import Iterator


def traverse(grid: list[list]) -> Iterator[tuple[int, int]]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            yield (i, j)


with open("input.txt") as f:
    # Add an extra border of dots around the original grid to avoid border conditions
    grid = [["."] + list(line.strip()) + ["."] for line in f]
    extra_row = [["."] * len(grid[0])]
    grid = extra_row + grid + extra_row

total_removed_rolls = 0
ongoing_removal = True

while ongoing_removal:
    # Mark for removal
    for i, j in traverse(grid):
        if grid[i][j] != "@":
            continue
        shifts = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),  # Skip 0, 0 shift
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        adjacent_rolls = 0
        for si, sj in shifts:
            if grid[i + si][j + sj] in ("@", "X"):
                adjacent_rolls += 1

        if adjacent_rolls < 4:
            grid[i][j] = "X"  # Mark for removal

    # Remove marked rolls
    removed_rolls = 0
    for i, j in traverse(grid):
        if grid[i][j] == "X":
            grid[i][j] = "."
            removed_rolls += 1

    ongoing_removal = removed_rolls > 0
    total_removed_rolls += removed_rolls

print(f"{total_removed_rolls=}")
