with open("input.txt") as f:
    pos = 50
    n_zeros = 0

    for line in f:
        signal = {"L": -1, "R": +1}[line[0]]
        turns = int(line[1:])
        pos = (pos + signal * turns) % 100
        print(f"{pos=}")
        if pos == 0:
            n_zeros += 1

    print(f"{n_zeros=}")
