from itertools import combinations
from math import dist

with open("input.txt") as f:
    coords = set(tuple(map(int, line.split(","))) for line in f)

pairs = sorted(combinations(coords, 2), key=lambda pair: dist(*pair))
circuits = {j: {j} for j in coords}

for j1, j2 in pairs:
    circuit = circuits[j1].union(circuits[j2])
    for jc in circuit:
        circuits[jc] = circuit

    circuits_ids = set(map(id, circuits.values()))
    if len(circuits_ids) == 1:
        break

prod_x = j1[0] * j2[0]

print(f"{prod_x=}")
