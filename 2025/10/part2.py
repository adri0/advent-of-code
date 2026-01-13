"""
vi = n0*b0i + ... + nm*bmi for i=0...k

V = [v0 ... vk]   -> target joltage per counter
N = [n0 ... nm]   -> number of presses per button
B = [b00 ... b0k] -> joltage addition per button per counter (binary matrix)
    [b10 ... b1k]
    [bm0 ... bjk]

k: number of joltage counters
m: number of buttons

Solve V = N * B , minimizing sum(ni) for i..m
"""

from pulp import LpMinimize, LpProblem, LpVariable, value

with open("input.txt") as f:
    machines = []
    for line in f:
        _, *buttons_input, target_input = line.split()
        target = tuple(map(int, target_input[1:-1].split(",")))
        buttons = [tuple(map(int, b[1:-1].split(","))) for b in buttons_input]
        machines.append((target, buttons))

total_presses = 0

for target, buttons in machines:
    k = len(target)
    m = len(buttons)

    V = target
    B = [[int(j in buttons[i]) for j in range(k)] for i in range(m)]

    N = [LpVariable(f"N_{i}", lowBound=0, cat="Integer") for i in range(m)]

    prob = LpProblem("Minimize_sum(N)", LpMinimize)
    prob += sum(N)

    # Constraints
    for i in range(k):
        prob += V[i] == sum(N[j] * B[j][i] for j in range(m))

    prob.solve()
    total_presses += sum(map(value, N))

print(f"{total_presses=}")
