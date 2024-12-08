from itertools import product
from operator import add, mul
from typing import Callable, NamedTuple

Operator = Callable[[int, int], int]


class Equation(NamedTuple):
    test_value: int
    numbers: list[int]


def read_input(path: str) -> list[Equation]:
    equations = []
    with open(path, "r") as f:
        for line in f:
            result, values = line.strip().split(": ")
            equation = Equation(
                test_value=int(result), numbers=list(map(int, values.split(" ")))
            )
            equations.append(equation)
    return equations


def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


def test_operators(equations: list[Equation], operators: list[Operator]) -> int:
    sum_val = 0
    for test_value, numbers in equations:
        for ops in product(operators, repeat=len(numbers) - 1):
            result = numbers[0]
            for i in range(len(numbers) - 1):
                result = ops[i](result, numbers[i + 1])
            if result == test_value:
                sum_val += test_value
                break
    return sum_val


def part1(equations: list[Equation]) -> int:
    return test_operators(equations, operators=[mul, add])


def part2(equations: list[Equation]) -> int:
    return test_operators(equations, operators=[mul, add, concat])


if __name__ == "__main__":
    equations = read_input("07/sample_input.txt")

    result1 = part1(equations)
    print(f"(part1) result: {result1}")

    result2 = part2(equations)
    print(f"(part2) result: {result2}")
