with open("input.txt") as f:
    ranges = f.read().strip().split(",")
    sum_invalid = 0

    for range_ in ranges:
        start, end = range_.split("-")
        for id_ in range(int(start), int(end) + 1):
            id = str(id_)
            first_half = id[: len(id) // 2]
            second_half = id[len(id) // 2 :]
            if first_half == second_half:
                sum_invalid += id_

    print(f"{sum_invalid=}")
