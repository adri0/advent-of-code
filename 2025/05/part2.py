from typing import NamedTuple


class Range(NamedTuple):
    start: int
    end: int


def overlap(r1: Range, r2: Range) -> bool:
    """Check if two ranges overlap"""
    r1, r2 = sorted([r1, r2])
    return (r2.start <= r1.end <= r2.end) or (r1.start <= r2.start <= r1.end)


def merge(r1: Range, r2: Range) -> Range:
    """Merge two overlapping ranges into a single range"""
    r1, r2 = sorted([r1, r2])
    return Range(min(r1.start, r2.start), max(r1.end, r2.end))


with open("input.txt") as f:
    ranges_, _ = f.read().strip().split("\n\n")
    ranges_input = [Range(*map(int, range_.split("-"))) for range_ in ranges_.split()]

ranges_non_overlapping: set[Range] = set()

while ranges_input:
    range_i = ranges_input.pop()
    for range_n_o in ranges_non_overlapping:
        if overlap(range_i, range_n_o):
            range_merged = merge(range_i, range_n_o)
            ranges_non_overlapping.remove(range_n_o)
            ranges_input.append(range_merged)
            break
    else:
        ranges_non_overlapping.add(range_i)

count_ids = sum(end - start + 1 for start, end in ranges_non_overlapping)

print(f"{count_ids=}")
