import re
from functools import cache
from typing import NamedTuple


class Record(NamedTuple):
    row: str
    groups: tuple[int, ...]


def read_records(path: str) -> list[Record]:
    with open(path) as f:
        return [
            Record(
                row=line[: line.find(" ")],
                groups=tuple(map(int, line[line.find(" ") :].split(","))),
            )
            for line in f
        ]


def record_is_valid(record: Record) -> bool:
    return record.groups == tuple(map(len, re.findall(r"#+", record.row)))


def drop_first_solved_group(record: Record) -> Record:
    if (
        record.groups
        and (match := re.match(r"^\.*#+(\.+|$)", record.row))
        and (count_char("#", match.group()) == record.groups[0])
    ):
        return Record(row=record.row[len(match.group()) :], groups=record.groups[1:])
    else:
        return record


def count_char(char: str, string: str):
    return sum(1 for ch in string if ch == char)


@cache
def count_valid_records(record: Record) -> int:
    if "?" in record.row:
        return sum(
            count_valid_records(drop_first_solved_group(next_rec))
            for next_rec in replace_next_unk(record)
            if is_viable(next_rec)  # reduce the search space
        )
    else:
        return int(record_is_valid(record))


def replace_next_unk(record: Record) -> tuple[Record, Record]:
    return (
        Record(record.row.replace("?", ".", 1), record.groups),
        Record(record.row.replace("?", "#", 1), record.groups),
    )


def is_viable(record: Record) -> bool:
    # Check the # groups already uncovered match the group number
    row_until_unk = record.row[: record.row.find("?") + 1]
    hash_groups_until_first_unk = tuple(filter(None, re.split(r"[\.]+", row_until_unk)))
    hash_counts = tuple(map(len, hash_groups_until_first_unk[:-1]))
    if hash_counts != record.groups[: len(hash_counts)]:
        return False

    # Check the first # group containing a ? is able to match first group count
    if (
        len(hash_groups_until_first_unk) > 0
        and "#" in hash_groups_until_first_unk[-1]
        and not (
            len(record.groups) >= len(hash_groups_until_first_unk)
            and count_char("#", hash_groups_until_first_unk[-1])
            <= record.groups[len(hash_groups_until_first_unk) - 1]
        )
    ):
        return False

    # Check if the number of ? is able to possibly match the group counts
    missing_dmg = sum(record.groups) - count_char("#", record.row)
    n_unknown = count_char("?", record.row)
    if missing_dmg > n_unknown or missing_dmg < 0:
        return False

    return True


def part1(records: list[Record]) -> None:
    count_per_row = list(map(count_valid_records, records))
    n = sum(count_per_row)
    print("(Part 1) Count per row:", count_per_row)
    print("(Part 1) Sum of valid counts:", n)


def unfold(record: Record) -> Record:
    return Record(row="?".join(5 * [record.row]), groups=record.groups * 5)


def part2(records: list[Record]) -> None:
    count_per_row = list(map(count_valid_records, map(unfold, records)))
    n = sum(count_per_row)
    print("(Part 2) Count per row:", count_per_row)
    print("(Part 2) Sum of valid counts:", n)


if __name__ == "__main__":
    records = read_records("example.txt")
    part1(records)
    part2(records)
