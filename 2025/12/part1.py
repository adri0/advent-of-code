with open("input.txt") as f:
    *_, regions = f.read().strip().split("\n\n")

possible = 0
for region in regions.strip().split("\n"):
    area, counts_input = region.split(": ")
    width, height = map(int, area.split("x"))
    total_presents = sum(map(int, counts_input.split()))
    occupied_area = total_presents * 9
    possible += int(occupied_area <= width * height)

print(f"{possible=}")
