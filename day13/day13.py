from functools import reduce
from operator import mul, add


def parse_list(list_string: str) -> list:
    assert list_string[0] == "[" and list_string[-1] == "]"
    result_list = []
    i_start = 1
    while i_start < len(list_string):
        match list_string[i_start]:
            case char if char.isnumeric():
                i_end = find_number_end(list_string, i_start)
                element = list_string[i_start : i_end]
                result_list.append(int(element))
            case "[":
                i_end = find_list_end(list_string, i_start)
                element = list_string[i_start : i_end]
                result_list.append(parse_list(element))
            case "" | "]":
                break
            case _:
                raise Exception(f"Cannot parse list from element: {element}")
        i_start += len(element) + 1
    return result_list


def find_number_end(string, number_start):
    return min(
        filter(
            lambda pos: pos > -1, [
                string.find(",", number_start),
                string.find("]", number_start)
            ]
        )
    )


def find_list_end(string, list_start):
    n_open_brackets = 0
    for i in range(list_start + 1, len(string)):
        if string[i] == "[":
            n_open_brackets += 1
        elif string[i] == "]":
            if n_open_brackets == 0:
                return i + 1
            else:
                n_open_brackets -= 1
    raise Exception(f"Unable to find list end for {string[list_start:]}")


def packets_in_order(left, right):
    match left, right:
        case int(left), int(right):
            if left != right:
                return left < right
        case list(left), list(right):
            for i in range(len(left)):
                if i >= len(right):
                    return False
                if (
                    left[i] != right[i] and
                    (res := packets_in_order(left[i], right[i])) is not None
                ):
                    return res
            if len(left) < len(right):
                return True
        case int(left), list(right):
            return packets_in_order([left], right)
        case list(left), int(right):
            return packets_in_order(left, [right])
        case _:
            raise Exception(f"Don't know how to compare: {left} - {right}")
    return None  # Unable to decide


packet_pairs = [
    list(map(parse_list, packet_pair_str.split()))
    for packet_pair_str in open("input.txt").read().split("\n\n")
]

sum_orderd_packet_pairs = sum(
    [
        i + 1
        for i, (left, right) in enumerate(packet_pairs) 
        if packets_in_order(left, right)
    ]
)

print("Sum of indices of ordered packets pairs:", sum_orderd_packet_pairs)


# -- Part 2 -- #

class Packet(list):
    def __lt__(self, other):
        return packets_in_order(self, other)


divider_packets = [[[2]], [[6]]]
all_packets = reduce(add, [[left] + [right] for left, right in packet_pairs])
sorted_packets = sorted(map(Packet, all_packets + divider_packets))

prod_divider_indices = reduce(
    mul, 
    [i + 1 for i, packet in enumerate(sorted_packets) if packet in divider_packets]
)

print("Product of divider packet indices:", prod_divider_indices)