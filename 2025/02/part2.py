from typing import Iterator


def slice_string(string: str) -> Iterator[list[str]]:
    """Generate string slices of length n. Start n=1 until n=len(string)-1"""
    for n in range(1, len(string)):
        if len(string) % n != 0:
            # Skip non divisable n
            continue

        slices = []
        num_slices = len(string) // n
        for i in range(num_slices):
            slice = string[n * i : n * (i + 1)]
            slices.append(slice)

        yield slices


with open("input.txt") as f:
    ranges = f.read().strip().split(",")
    sum_invalid = 0

    for range_ in ranges:
        start, end = range_.split("-")
        for id_ in range(int(start), int(end) + 1):
            id = str(id_)
            for slices in slice_string(id):
                if len(slices) > 1 and len(set(slices)) == 1:
                    sum_invalid += id_
                    break

    print(f"{sum_invalid=}")
