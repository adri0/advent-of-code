from math import prod

with open("input.txt") as f:
    lines = f.read().strip().split("\n")

operators = lines[-1].split()
value_rows = [list(map(int, line.split())) for line in lines[:-1]]

total_sum = 0
for i, op in enumerate(operators):
    values = [row[i] for row in value_rows]
    if op == "*":
        total_sum += prod(values)
    elif op == "+":
        total_sum += sum(values)
    else:
        raise ValueError("Unexpected operator '{op}'")

print(f"{total_sum=}")
