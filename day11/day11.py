from dataclasses import dataclass
import operator


input_str = open("input.txt").read()
monkeys_input = input_str.split("\n\n")


@dataclass
class Monkey:
    index: int
    items: list[int] 
    operation: callable
    divisable_by: int
    monkey_div_true: int
    monkey_div_false: int
    inspection_count: int = 0

    def next_monkey(self, item_worry) -> int:
        if is_divisable_by(item_worry, self.divisable_by):
            return self.monkey_div_true 
        else:
            return self.monkey_div_false

    def inspect_next(self):
        while self.items:
            self.inspection_count += 1
            item_worry = self.items.pop(0)
            item_worry = self.operation(item_worry)
            item_worry = item_worry // 3
            yield item_worry, self.next_monkey(item_worry)


known_divisables = {}
def is_divisable_by(num, divisor):
    if (num, divisor) in known_divisables:
        return known_divisables[(num, divisor)]
    else:
        num_is_divisable = num % divisor == 0
        known_divisables[(num, divisor)] = num_is_divisable
        return num_is_divisable


def parse_operation(op_string):
    parts = op_string.split()
    num1 = int(parts[2]) if parts[2].isnumeric() else None
    num2 = int(parts[4]) if parts[4].isnumeric() else None
    op = {"*": operator.mul, "+": operator.add}[parts[3]]
    def operation(old):
        return op(num1 or old, num2 or old)
    return operation


def parse_monkey_str(monkey_as_str) -> Monkey:
    lines = list(map(lambda s: s.strip(), monkey_as_str.split("\n")))
    return Monkey(
        index=int(lines[0][len("Monkey ") : -1]),
        items=list(map(int, lines[1][len("Starting items: "):].split(", "))),
        operation=parse_operation(lines[2][len("Operation: "):]),
        divisable_by=int(lines[3][len("Test: divisable by "):]),
        monkey_div_true=int(lines[4][len("If true: throw to monkey "):]),
        monkey_div_false=int(lines[5][len("If false: throw to monkey "):])
    )


monkeys = list(map(parse_monkey_str, monkeys_input))


def do_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        for item_worry, next_monkey in monkey.inspect_next():
            monkeys[next_monkey].items.append(item_worry)


def print_monkeys(monkeys):
    print("\n".join([f"Monkey {m.index}: {m.items}, {m.inspection_count}" for m in monkeys]))


# print_monkeys(monkeys)

for _ in range(20):
    do_round(monkeys)

# print_monkeys(monkeys)

def monkey_biz(monkeys):
    ins_count1, ins_count2 = sorted([monkey.inspection_count for monkey in monkeys])[-2:]
    return ins_count1 * ins_count2


print("Monkey biz:", monkey_biz(monkeys))
