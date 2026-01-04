with open("input.txt") as f:
    total_joltage = 0

    for line in f:
        bank = line.strip()

        first_highest = 0
        for i, value in enumerate(bank[: len(bank) - 1]):
            if int(value) > first_highest:
                first_highest = int(value)

                second_highest = 0
                for sec_value in bank[i + 1 :]:
                    if int(sec_value) > second_highest:
                        second_highest = int(sec_value)

        total_joltage += int(f"{first_highest}{second_highest}")

    print(f"{total_joltage=}")
