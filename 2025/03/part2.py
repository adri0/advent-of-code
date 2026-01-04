def find_highest_n(bank: str, n: int) -> int:
    """Recursively finds the highest n digits"""
    first_highest = 0

    i_highest = -1
    bank_portion_for_highest_first = bank[: len(bank) - n + 1]
    for i, value in enumerate(bank_portion_for_highest_first):
        if int(value) > first_highest:
            first_highest = int(value)
            i_highest = i

    if n > 1:
        remaining_bank = bank[i_highest + 1 :]
        remaining_highest = find_highest_n(remaining_bank, n=n - 1)
        return int(f"{first_highest}{remaining_highest}")
    else:
        return first_highest


with open("input.txt") as f:
    total_joltage = 0

    for line in f:
        bank = line.strip()
        total_joltage += find_highest_n(bank, n=12)

    print(f"{total_joltage=}")
