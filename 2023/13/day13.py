def read_mirrors(input_path: str) -> list[list[str]]:
    with open(input_path) as f:
        return [block.split() for block in f.read().strip().split("\n\n")]


def rows_up_reflection(block: list[str], sumdge_fix: bool = False) -> int:
    # Find reflection (there might be more than 1)
    for line in range(len(block) - 1):
        smudge_fixed = not sumdge_fix

        # if not smudge_fixed and :
        if block[line] != block[line + 1]:  # Not a possible reflection
            continue
        # elif not smudge_fixed and

        # iterate from the reflection
        refl_i = line  # backward
        refl_j = line + 1  # forward
        while 0 <= refl_i and refl_j < len(block):
            if block[refl_i] != block[refl_j]:
                break

            refl_i -= 1
            refl_j += 1
        else:
            return line + 1  # Didn't break thus valid reflection

    return 0


def cols_left_reflection(block: list[str], sumdge_fix: bool = False) -> int:
    block_transposed = [
        "".join(block[i_row][i_col] for i_row in range(len(block)))
        for i_col in range(len(block[0]))
    ]
    return rows_up_reflection(block_transposed, sumdge_fix=sumdge_fix)


def diff(str1: str, str2: str) -> int:
    if len(str1) != len(str2):
        raise ValueError("Length must be the same")
    return sum(1 for i in range(len(str1)) if str1[i] != str2[i])


def part1(mirrors: list[list[str]]) -> None:
    res = sum(
        cols_left_reflection(block) + 100 * rows_up_reflection(block)
        for block in mirrors
    )
    print("(Part 1) Result:", res)


def part2(mirrors: list[list[str]]) -> None:
    res = sum(
        cols_left_reflection(block, sumdge_fix=True)
        + 100 * rows_up_reflection(block, sumdge_fix=True)
        for block in mirrors
    )
    print("(Part 2) Result:", res)


if __name__ == "__main__":
    mirrors = read_mirrors("input.txt")
    part1(mirrors)
    # part2(mirrors)
