DIGIT_NAME_MAP: dict[str, str] = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

ALL_DIGITS: list[str] = list(DIGIT_NAME_MAP.keys()) + list(DIGIT_NAME_MAP.values())


def get_calibration_codes(input_path: str) -> list[int]:
    codes = []
    with open(input_path, "r") as f:
        for line in f:
            first = find_first_digit(line)
            last = find_first_digit(line, from_right=True)
            code = int(f"{digit_to_num(first)}{digit_to_num(last)}")
            codes.append(code)
    return codes


def find_first_digit(line: str, from_right: bool = False) -> str:
    if not from_right:
        find_first = str.find
        cur_position = len(line) + 1
        is_pos_before = lambda pos, ref: -1 < pos < ref
    else:
        find_first = str.rfind
        cur_position = -1
        is_pos_before = lambda pos, ref: pos > ref

    first_digit = ""
    for digit in ALL_DIGITS:
        pos = find_first(line, digit)
        if is_pos_before(pos, cur_position):
            cur_position = pos
            first_digit = digit

    return first_digit


def digit_to_num(digit: str) -> str:
    return DIGIT_NAME_MAP.get(digit, digit)


if __name__ == "__main__":
    codes = get_calibration_codes("input.txt")
    codes_sum = sum(codes)
    print("Calibration codes:")
    print(codes)
    print()
    print("Sum of codes:")
    print(codes_sum)
