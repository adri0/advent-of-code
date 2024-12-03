import re


def read_input(path: str) -> str:
    with open(path, "r") as f:
        return f.read().strip()


def part1(memory: str) -> int:
    result = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    for match in re.finditer(pattern, memory):
        a, b = map(int, match.groups())
        result += a * b
    return result


def part2(memory: str) -> int:
    result = 0
    do = True
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)"
    for match in re.finditer(pattern, memory):
        cmd = match.group()
        if cmd.startswith("mul") and do:
            a, b = map(int, match.groups())
            result += a * b
        elif cmd == "do()":
            do = True
        elif cmd == "don't()":
            do = False
    return result


if __name__ == "__main__":
    memory = read_input("03/input.txt")

    res1 = part1(memory)
    print(f"(part1) result: {res1}")

    res2 = part2(memory)
    print(f"(part2) result: {res2}")
