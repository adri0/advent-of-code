from math import prod

with open("input.txt") as f:
    # Add an extra empty column at the end of all rows
    *value_rows, operator_row = [line + " " for line in f.read().split("\n")]

total = 0
operands: list[int] = []
operator = ""

for i in range(len(operator_row)):
    if operator_row[i] in ("*", "+"):
        operator = operator_row[i]

    operand = "".join([value[i] for value in value_rows]).strip()

    if not operand:  # Empty column
        if operator == "*":
            total += prod(operands)
        elif operator == "+":
            total += sum(operands)
        else:
            raise ValueError("Unexpected operator '{operator}'")
        operands = []
    else:
        operands.append(int(operand))

print(f"{total=}")
