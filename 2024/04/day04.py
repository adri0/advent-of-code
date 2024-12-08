from typing import Iterator


def read_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f]


def traverse(input: list[str]) -> Iterator[tuple[int, int]]:
    for i in range(len(input)):
        for j in range(len(input[i])):
            yield (i, j)


def part1(input: list[str]) -> int:
    result = 0
    for i, j in traverse(input):
        if input[i][j] == "X":
            result += count_xmas(i, j, input)
    return result


def count_xmas(i: int, j: int, input: list[str]) -> int:
    n_xmas = 0
    for m in (0, 1, -1):
        for n in (0, 1, -1):
            word = ""
            for k in range(4):
                word += get_char(i + m * k, j + n * k, input)
            n_xmas += int(word == "XMAS")
    return n_xmas


def part2(input: list[str]) -> int:
    result = 0
    for i, j in traverse(input):
        if input[i][j] == "A":
            result += count_x_mas(i, j, input)
    return result


def count_x_mas(i: int, j: int, input: list[str]) -> int:
    n_mas = 0
    x_edges = [
        ((-1, -1), (1, 1)),
        ((-1, 1), (1, -1)),
        ((1, 1), (-1, -1)),
        ((1, -1), (-1, 1)),
    ]
    for (k, l), (m, n) in x_edges:
        word = (
            get_char(i + k, j + l, input) + input[i][j] + get_char(i + m, j + n, input)
        )
        n_mas += int(word == "MAS")
    return int(n_mas == 2)


def get_char(i: int, j: int, input: list[str]) -> str:
    if i < 0 or j < 0 or i >= len(input) or j >= len(input[i]):
        return ""
    else:
        return input[i][j]


if __name__ == "__main__":
    input = read_input("04/sample_input.txt")

    res1 = part1(input)
    print(f"(part1) result: {res1}")

    res2 = part2(input)
    print(f"(part2) result: {res2}")
