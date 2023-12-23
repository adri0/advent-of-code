import re
from collections import defaultdict


def read_initialization_sequence(input_path: str) -> list[str]:
    with open(input_path) as f:
        return f.read().strip().split(",")


def hash_algo(string: str) -> int:
    hash_val = 0
    for char in string:
        hash_val += ord(char)
        hash_val = hash_val * 17
        hash_val = hash_val % 256
    return hash_val


def part1(ini_seq: list[str]) -> None:
    hash_sum = sum(map(hash_algo, ini_seq))
    print("(Part 1) Hash sum:", hash_sum)


def part2(ini_seq: list[str]) -> None:
    boxes: dict[int, list[str]] = defaultdict(list)
    labels: dict[str, int] = {}

    for command in ini_seq:
        lens, focus_len = re.split(r"-|=", command)
        box_num = hash_algo(lens)

        if focus_len.isnumeric():
            if lens not in boxes[box_num]:
                boxes[box_num].append(lens)
            labels[lens] = int(focus_len)
        elif focus_len == "" and lens in labels:
            labels.pop(lens)
            boxes[box_num].remove(lens)
        else:
            raise ValueError("Bug!")

    focusing_power = 0
    for lens, label in labels.items():
        box_num = hash_algo(lens)
        box_slot = boxes[box_num].index(lens) + 1
        focusing_power += (box_num + 1) * box_slot * label

    print("(Part 2) Focusing power:", focusing_power)


if __name__ == "__main__":
    ini_seq = read_initialization_sequence("input.txt")
    part1(ini_seq)
    part2(ini_seq)
