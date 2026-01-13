from itertools import combinations_with_replacement

with open("input.txt") as f:
    machines = []
    for line in f:
        indicator_str, *buttons_str, _ = line.split()
        target: list[bool] = [{".": False, "#": True}[c] for c in indicator_str[1:-1]]
        buttons = [tuple(map(int, b[1:-1].split(","))) for b in buttons_str]
        machines.append((target, buttons))

min_pushes = 0
for target, buttons in machines:
    for n_pushes in range(1, 100):
        for button_combination in combinations_with_replacement(buttons, n_pushes):
            indicator = [False] * len(target)

            for button in button_combination:
                for pos in button:
                    indicator[pos] = not (indicator[pos])

            if indicator == target:
                min_pushes += n_pushes
                break
        else:
            # Unable to find in n_push
            continue
        break
    else:
        raise ValueError("Couldn't find it")

print(f"{min_pushes=}")
