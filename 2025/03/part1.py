with open("input.txt") as f:
    total_joltage = 0

    for line in f:
        bank = line.strip()

        first_highest = 0
        i_highest = -1
        for i, value in enumerate(bank[: len(bank) - 1]):
            if int(value) > first_highest:
                first_highest = int(value)
                i_highest = i

        second_highest = max(bank[i_highest + 1 :])
        total_joltage += int(f"{first_highest}{second_highest}")

    print(f"{total_joltage=}")
