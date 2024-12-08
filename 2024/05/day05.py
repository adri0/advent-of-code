from collections import defaultdict
from functools import partial

Rules = defaultdict[int, set[int]]
Update = list[int]


def read_input(path: str) -> tuple[Rules, list[Update]]:
    with open(path, "r") as f:
        rules_section, updates_section = f.read().split("\n\n")

    rules = Rules(set[int])
    for line in rules_section.split():
        prev, after = map(int, line.split("|"))
        rules[prev].add(after)

    updates = [Update(map(int, line.split(","))) for line in updates_section.split()]
    return rules, updates


def part1(rules: Rules, updates: list[Update]) -> int:
    mid_sum = sum(
        update[len(update) // 2]
        for update in updates
        if is_correctly_ordered(update, rules)
    )
    return mid_sum


def is_correctly_ordered(update: Update, rules: Rules) -> bool:
    seen: set[int] = set()
    for page_num in update:
        if seen & rules[page_num]:
            return False
        seen.add(page_num)
    return True


def part2(rules: Rules, updates: list[Update]) -> int:
    mid_sum = 0
    for update in updates:
        if not is_correctly_ordered(update, rules):
            sorted_update = sorted(update, key=partial(SortablePage, rules=rules))
            mid_sum += sorted_update[len(sorted_update) // 2]
    return mid_sum


class SortablePage:
    def __init__(self, num: int, rules: Rules):
        self.num = num
        self.rules = rules

    def __lt__(self, other: "SortablePage") -> bool:
        return other.num in self.rules[self.num]


if __name__ == "__main__":
    rules, updates = read_input("05/input.txt")

    res1 = part1(rules, updates)
    print(f"(part1) result: {res1}")

    res2 = part2(rules, updates)
    print(f"(part1) result: {res2}")
