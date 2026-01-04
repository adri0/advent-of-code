def find_highest_battery_sequence(bank: str, n: int) -> int:
    """
    Recursively finds the highest number that can be formed
    from a (not necessarily consecutive) sequence of n digits.
    """
    first_digit = 0
    i_first: int
    # The last n - 1 digits are not eligible candidates for first digit
    bank_slice = bank[: len(bank) - (n - 1)]
    for i, digit in enumerate(bank_slice):
        if int(digit) > first_digit:
            first_digit = int(digit)
            i_first = i

    if n == 1:
        return first_digit
    else:
        remaining_bank = bank[i_first + 1 :]
        remaining_sequence = find_highest_battery_sequence(remaining_bank, n=n - 1)
        return int(f"{first_digit}{remaining_sequence}")


with open("input.txt") as f:
    total_joltage = 0
    for line in f:
        bank = line.strip()
        total_joltage += find_highest_battery_sequence(bank, n=12)
    print(f"{total_joltage=}")
