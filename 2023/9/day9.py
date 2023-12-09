def read_histories(input_path: str) -> list[list[int]]:
    with open(input_path) as f:
        return [list(map(int, line.strip().split())) for line in f.readlines()]


def extrapolate(series: list[int]) -> int:
    diff = [series[i + 1] - series[i] for i in range(len(series) - 1)]
    if all(val == 0 for val in diff):
        return series[-1]
    new_val = extrapolate(diff)
    return series[-1] + new_val


def part1(histories: list[list[int]]) -> None:
    sum_new_val = sum(map(extrapolate, histories))
    print("(Part 1) Sum extrapolated values:", sum_new_val)


def part2(histories: list[list[int]]) -> None:
    sum_new_val = sum(extrapolate(list(reversed(history))) for history in histories)
    print("(Part 2) Sum extrapolated start values:", sum_new_val)


if __name__ == "__main__":
    histories = read_histories("input.txt")
    part1(histories)
    part2(histories)
