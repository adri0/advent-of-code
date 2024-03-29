from dataclasses import dataclass
from functools import reduce
import operator


@dataclass
class Monkey:
    index: int
    items: list[int]
    operation: callable
    divisor: int
    monkey_div_true: int
    monkey_div_false: int
    inspection_count: int = 0
    common_divisor = None

    def next_monkey(self, item_worry) -> int:
        if item_worry % self.divisor == 0:
            return self.monkey_div_true
        else:
            return self.monkey_div_false

    def inspect_next(self):
        while self.items:
            self.inspection_count += 1
            item_worry = self.items.pop(0)
            item_worry = self.operation(item_worry)
            item_worry = item_worry % Monkey.common_divisor
            yield item_worry, self.next_monkey(item_worry)


def parse_operation(op_string):
    """Parse a string like 'new = old * 3' into a function"""
    parts = op_string.split()
    num1 = int(parts[2]) if parts[2].isnumeric() else None
    num2 = int(parts[4]) if parts[4].isnumeric() else None
    op = {"*": operator.mul, "+": operator.add}[parts[3]]

    def operation(old):
        return op(num1 or old, num2 or old)

    return operation


def parse_monkey_str(monkey_as_str: str) -> Monkey:
    lines = [line.strip() for line in monkey_as_str.split("\n")]
    return Monkey(
        index=int(lines[0][len("Monkey ") : -1]),
        items=list(map(int, lines[1][len("Starting items: ") :].split(", "))),
        operation=parse_operation(lines[2][len("Operation: ") :]),
        divisor=int(lines[3][len("Test: divisable by ") :]),
        monkey_div_true=int(lines[4][len("If true: throw to monkey ") :]),
        monkey_div_false=int(lines[5][len("If false: throw to monkey ") :]),
    )


def do_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        for item_worry, next_monkey in monkey.inspect_next():
            monkeys[next_monkey].items.append(item_worry)


def monkey_biz(monkeys, n_rounds):
    for _ in range(n_rounds):
        do_round(monkeys)
    i1, i2 = sorted(monkey.inspection_count for monkey in monkeys)[-2:]
    return i1 * i2


def get_monkeys(input_path="input.txt"):
    input_str = open(input_path).read()
    monkeys = list(map(parse_monkey_str, input_str.split("\n\n")))
    Monkey.common_divisor = reduce(
        operator.mul, set(monkey.divisor for monkey in monkeys)
    )
    return monkeys


print("Monkey biz (10 rounds):", monkey_biz(get_monkeys(), n_rounds=10))
print("Monkey biz (10_000 rounds):", monkey_biz(get_monkeys(), n_rounds=10_000))
