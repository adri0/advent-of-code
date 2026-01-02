with open("input.txt") as f:
    dial_pos = 50
    n_zero = 0

    for line in f:
        signal = {"L": -1, "R": +1}[line[0]]
        turns = int(line[1:])

        line_pos = dial_pos + signal * turns
        dial_pos_after = line_pos % 100
        zero_crossings = 0
        if line_pos <= 0 and dial_pos != 0:
            zero_crossings += 1

        zero_crossings += abs(line_pos) // 100

        n_zero += zero_crossings
        print(f"{dial_pos=}\t{line_pos=}\t{dial_pos_after=}\t{zero_crossings=}")

        dial_pos = dial_pos_after

    print(f"{n_zero=}")
