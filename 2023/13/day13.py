def read_mirrors(input_path: str) -> list[list[str]]:
    with open(input_path) as f:
        return [block.split() for block in f.read().strip().split("\n\n")]


def nrows_up_of_reflection(block: list[str], fix_smudge: bool = False) -> int:
    # Find reflection line index
    for i_line in range(len(block) - 1):
        smudge_fixed = not fix_smudge

        if not smudge_fixed and diff(block[i_line], block[i_line + 1]) == 1:
            smudge_fixed = True
        elif block[i_line] != block[i_line + 1]:  # Not a possible reflection
            continue

        # iterate from the reflection
        i_back = i_line - 1  # backward
        i_forw = i_line + 2  # forward
        while 0 <= i_back and i_forw < len(block):
            if not smudge_fixed and diff(block[i_back], block[i_forw]) == 1:
                smudge_fixed = True
            elif block[i_back] != block[i_forw]:
                break

            i_back -= 1
            i_forw += 1
        else:
            if not fix_smudge or smudge_fixed:
                return i_line + 1  # Valid reflection
    return 0


def ncols_left_of_reflection(block: list[str], fix_smudge: bool = False) -> int:
    block_transposed = [
        "".join(block[i_row][i_col] for i_row in range(len(block)))
        for i_col in range(len(block[0]))
    ]
    return nrows_up_of_reflection(block_transposed, fix_smudge=fix_smudge)


def diff(str1: str, str2: str) -> int:
    return sum(1 for i in range(len(str1)) if str1[i] != str2[i])


def part1(mirrors: list[list[str]]) -> None:
    res = sum(
        ncols_left_of_reflection(block) + 100 * nrows_up_of_reflection(block)
        for block in mirrors
    )
    print("(Part 1) Result:", res)


def part2(mirrors: list[list[str]]) -> None:
    res = sum(
        ncols_left_of_reflection(block, fix_smudge=True)
        + 100 * nrows_up_of_reflection(block, fix_smudge=True)
        for block in mirrors
    )
    print("(Part 2) Result:", res)


if __name__ == "__main__":
    mirrors = read_mirrors("input.txt")
    part1(mirrors)
    part2(mirrors)
