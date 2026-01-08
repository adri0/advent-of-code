from itertools import combinations
from math import dist, prod

with open("input.txt") as f:
    coords = set(tuple(map(int, line.strip().split(","))) for line in f)

pairs = sorted(combinations(coords, 2), key=lambda pair: dist(*pair))
circuits = {j: {j} for j in coords}
for j1, j2 in pairs[:1000]:
    circuit = circuits[j1].union(circuits[j2])
    for jc in circuit:
        circuits[jc] = circuit

unique_circuits = set(map(tuple, circuits.values()))
largest_circuits_len = sorted(map(len, unique_circuits))[-3:]
product_largest = prod(largest_circuits_len)

print(f"{product_largest=}")
