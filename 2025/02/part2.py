from typing import Generator


def generate_char_seqs(string: str) -> Generator[list[str], None, None]:
    """Generate string slices of length n. Start n=1 until n=len(id)"""
    for n in range(1, len(string)):
        if len(string) % n != 0:
            # Skip non divisable n
            continue

        slices = []
        n_slices = len(string) // n
        for i in range(n_slices):
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
            for char_seqs in generate_char_seqs(id):
                if len(char_seqs) > 1 and len(set(char_seqs)) == 1:
                    sum_invalid += id_
                    break

    print(f"{sum_invalid=}")
