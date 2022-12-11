input_moves = [line.strip() for i, line in enumerate(open("input.txt")) if i > 9]


def initiate_stacks():
    return list(map(list, [
        "ZTFRWJG",
        "GWM",
        "JNHG",
        "JRCNW",
        "WFSBGQVM",
        "SRTDVWC",
        "HBNCDZGV",
        "SJNMGC",
        "GPNWCJDL"
    ]))


stacks = initiate_stacks()


def do_move(stacks, n_blocks, from_stack_i, to_stack_i):
    from_stack = stacks[from_stack_i-1]
    to_stack = stacks[to_stack_i-1]
    for _ in range(n_blocks):
        to_stack.append(from_stack.pop())


for move_line in input_moves:
    line_parts = move_line.split()
    n_blocks = int(line_parts[1])
    from_stack_i = int(line_parts[3])
    to_stack_i = int(line_parts[5])
    do_move(stacks, n_blocks, from_stack_i, to_stack_i)


result1 = "".join(map(lambda s: s[-1], stacks[1:]))
print(result1)


# -- Part 2 -- #

stacks = initiate_stacks()

def do_move_multiple(stacks, n_blocks, from_stack_i, to_stack_i):
    from_stack = stacks[from_stack_i-1]
    to_stack = stacks[to_stack_i-1]
    popped = [from_stack.pop() for _ in range(n_blocks)]
    popped.reverse()
    to_stack.extend(popped)

for move_line in input_moves:
    line_parts = move_line.split()
    n_blocks = int(line_parts[1])
    from_stack_i = int(line_parts[3])
    to_stack_i = int(line_parts[5])
    do_move_multiple(stacks, n_blocks, from_stack_i, to_stack_i)


result2 = "".join(map(lambda s: s[-1], stacks[1:]))
print(result2)