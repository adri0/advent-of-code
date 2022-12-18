from functools import reduce
from operator import mul, add
import json


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
    list(map(json.loads, packet_pair_str.split()))
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