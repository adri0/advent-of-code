from itertools import combinations_with_replacement

with open("input.txt") as f:
    machines = []
    for line in f:
        indicator_str, *buttons_str, _ = line.split()
        goal_state: list[bool] = [
            {".": False, "#": True}[c] for c in indicator_str[1:-1]
        ]
        buttons = [tuple(map(int, b[1:-1].split(","))) for b in buttons_str]
        machines.append((goal_state, buttons))

min_pushes = 0
for goal_state, buttons in machines:
    for n_pushes in range(1, 100):
        for button_presses in combinations_with_replacement(buttons, n_pushes):
            indicator = [False] * len(goal_state)

            for positions in button_presses:
                for i in positions:
                    indicator[i] = not (indicator[i])

            if indicator == goal_state:
                min_pushes += n_pushes
                break
        else:
            # Unable to find in n_push
            continue
        break
    else:
        raise ValueError("Couldn't find it")

print(f"{min_pushes=}")
