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


def read_packet_pairs(input_path):
    return [
        list(map(json.loads, packet_pair_str.split()))
        for packet_pair_str in open(input_path).read().split("\n\n")
    ]


def sum_pairs_in_order(packet_pairs):
    return sum(
        [
            i + 1
            for i, (left, right) in enumerate(packet_pairs) 
            if packets_in_order(left, right)
        ]
    )


def part1(input_path):
    packet_pairs = read_packet_pairs(input_path)
    result = sum_pairs_in_order(packet_pairs)
    print("Sum of indices of pairs in order:", result)


class Packet(list):
    def __lt__(self, other):
        return packets_in_order(self, other)


DIVIDER_PACKETS = [[[2]], [[6]]]


def sort_packets(packet_pairs):
    return sorted(map(Packet, reduce(add, packet_pairs) + DIVIDER_PACKETS))


def prod_divider_indices(sorted_packets):
    return reduce(
        mul, 
        [
            i + 1 
            for i, packet in enumerate(sorted_packets) 
            if packet in DIVIDER_PACKETS
        ]
    )


def part2(input_path):
    packet_pairs = read_packet_pairs(input_path)
    sorted_packets = sort_packets(packet_pairs)
    result = prod_divider_indices(sorted_packets)
    print("Product of divider packet indices:", result)


input_path = "input.txt"
part1(input_path)
part2(input_path)