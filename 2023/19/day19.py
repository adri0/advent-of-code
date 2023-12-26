import re
from typing import NamedTuple, Optional


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


class Operation(NamedTuple):
    operator: str
    numerator: int

    def __call__(self, in_: int) -> bool:
        return {">": in_ > self.numerator, "<": in_ < self.numerator}[self.operator]


class Rule(NamedTuple):
    category: Optional[str]
    operation: Optional[Operation]
    next_step: str


class Workflow(NamedTuple):
    name: str
    rules: list[Rule]


RULE_STMT_PATTERN = (
    r"((?P<category>\w+)(?P<operator>\>|\<)(?P<numerator>\d+)\:)?(?P<next_step>\w+)"
)


def parse_workflow(line: str) -> Workflow:
    rules_stmts = line[line.index("{") + 1 : line.index("}")]
    return Workflow(
        name=line[: line.index("{")],
        rules=[
            Rule(
                category=match.group("category"),
                operation=Operation(
                    match.group("operator"), int(match.group("numerator"))
                )
                if match.group("operator") and match.group("numerator")
                else None,
                next_step=match.group("next_step"),
            )
            for match in re.finditer(RULE_STMT_PATTERN, rules_stmts)
        ],
    )


def read_workflows_and_parts(input_path: str) -> tuple[dict[str, Workflow], list[Part]]:
    with open(input_path) as f:
        block_workf, block_parts = f.read().split("\n\n")
    workflows = {wf.name: wf for wf in map(parse_workflow, block_workf.split())}
    parts = [Part(*map(int, re.findall(r"\d+", line))) for line in block_parts.split()]
    return workflows, parts


def part1(workflows: dict[str, Workflow], parts: list[Part]) -> None:
    accepted_parts = []
    for part in parts:
        input_ = "in"
        while input_ not in ("A", "R"):
            for rule in workflows[input_].rules:
                rule_passes = (
                    not rule.category
                    or not rule.operation
                    or rule.operation(part._asdict()[rule.category])
                )
                if rule_passes:
                    input_ = rule.next_step
                    break
            else:
                raise ValueError(f"No rule for part: {rule} {part}")
        if input_ == "A":
            accepted_parts.append(part)

    sum_acc = sum(part.x + part.m + part.a + part.s for part in accepted_parts)

    print("(Part 1) Sum accepted parts", sum_acc)


class PartsRanges(NamedTuple):
    cur_step: str
    x: range = range(1, 4001)
    m: range = range(1, 4001)
    a: range = range(1, 4001)
    s: range = range(1, 4001)


def split_range(range_: range, n: int) -> tuple[range, range]:
    return range(range_.start, n), range(n, range_.stop)


def part2(workflows: dict[str, Workflow]) -> None:
    accepted_combinations = 0
    parts_ranges = [PartsRanges(cur_step="in")]
    while parts_ranges:
        cur_pr = parts_ranges.pop()
        if cur_pr.cur_step == "A":
            accepted_combinations += (
                len(cur_pr.x) * len(cur_pr.m) * len(cur_pr.a) * len(cur_pr.s)
            )
        elif cur_pr.cur_step == "R":
            continue
        else:
            for rule in workflows[cur_pr.cur_step].rules:
                cur_pr_params, next_pr_params = cur_pr._asdict(), cur_pr._asdict()
                next_pr_params["cur_step"] = rule.next_step

                if rule.operation and rule.category:
                    range_ = cur_pr_params[rule.category]
                    if rule.operation.operator == ">":
                        (
                            cur_pr_params[rule.category],
                            next_pr_params[rule.category],
                        ) = split_range(range_, rule.operation.numerator + 1)
                    elif rule.operation.operator == "<":
                        (
                            next_pr_params[rule.category],
                            cur_pr_params[rule.category],
                        ) = split_range(range_, rule.operation.numerator)
                    else:
                        raise ValueError("Shouldn't happen")

                cur_pr = PartsRanges(**cur_pr_params)
                next_pr = PartsRanges(**next_pr_params)

                parts_ranges.append(next_pr)

    print("(Part 2) Accepted combinations", accepted_combinations)


if __name__ == "__main__":
    workflows, parts = read_workflows_and_parts("input.txt")
    part1(workflows, parts)
    part2(workflows)
