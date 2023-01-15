input_list = [line.strip() for line in open("input.txt")]


def parse_interval(interval_str):
    start, end = interval_str.split("-")
    return range(int(start), int(end) + 1)


def parse_interval_pair(interval_pair_str):
    return tuple(map(parse_interval, interval_pair_str.split(",")))


def fully_contains(inter1, inter2):
    overlap = set(inter1).intersection(set(inter2))
    return overlap == set(inter1) or overlap == set(inter2)


interval_pairs_list = map(parse_interval_pair, input_list)
result1 = sum(fully_contains(pair[0], pair[1]) for pair in interval_pairs_list)
print(result1)


def has_overlap(inter1, inter2):
    overlap = set(inter1).intersection(set(inter2))
    return len(overlap) > 0


interval_pairs_list = map(parse_interval_pair, input_list)
result2 = sum(has_overlap(pair[0], pair[1]) for pair in interval_pairs_list)
print(result2)
