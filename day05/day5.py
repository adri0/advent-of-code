from typing import Callable


Stacks = list[list[str]]


def initiate_stacks() -> Stacks:
    stacks_as_str = [
        "ZTFRWJG",
        "GWM",
        "JNHG",
        "JRCNW",
        "WFSBGQVM",
        "SRTDVWC",
        "HBNCDZGV",
        "SJNMGC",
        "GPNWCJDL",
    ]
    return list(map(list, stacks_as_str))  # type: ignore


def move_one_at_time(stacks: Stacks, n_blocks: int, stack1: int, stack2: int) -> None:
    from_stack = stacks[stack1 - 1]
    to_stack = stacks[stack2 - 1]
    for _ in range(n_blocks):
        to_stack.append(from_stack.pop())


def move_n_at_time(stacks: Stacks, n_blocks: int, stack1: int, stack2: int) -> None:
    from_stack = stacks[stack1 - 1]
    to_stack = stacks[stack2 - 1]
    popped = [from_stack.pop() for _ in range(n_blocks)]
    popped.reverse()
    to_stack.extend(popped)


def apply_moves(stacks: Stacks, moves: list[str], move_func: Callable) -> None:
    for move_line in moves:
        line_parts = move_line.split()
        n_blocks = int(line_parts[1])
        from_stack_i = int(line_parts[3])
        to_stack_i = int(line_parts[5])
        move_func(stacks, n_blocks, from_stack_i, to_stack_i)


def get_stack_tops(stacks: Stacks):
    return "".join(map(lambda s: s[-1], stacks[1:]))


def part1(moves: list[str]) -> None:
    stacks = initiate_stacks()
    apply_moves(stacks, moves, move_one_at_time)
    print("Stack tops moving one at a time:", get_stack_tops(stacks))


def part2(moves: list[str]) -> None:
    stacks = initiate_stacks()
    apply_moves(stacks, moves, move_n_at_time)
    print("Stack tops moving multiple at a time:", get_stack_tops(stacks))


if __name__ == "__main__":
    moves = [line.strip() for i, line in enumerate(open("input.txt")) if i > 9]
    part1(moves)
    part2(moves)
