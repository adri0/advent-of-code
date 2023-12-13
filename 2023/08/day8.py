import math
import re
from itertools import cycle
from typing import NamedTuple


class Node(NamedTuple):
    name: str
    left: str
    right: str


class Map(NamedTuple):
    directions: str
    nodes: dict[str, Node]  # node name -> node


def read_map(input_path: str) -> Map:
    with open(input_path) as f:
        lines = f.readlines()
    return Map(
        directions=lines[0].strip(),
        nodes={
            line[:3]: Node(name=line[:3], left=line[7:10], right=line[12:15])
            for line in lines[2:]
        },
    )


def steps_until_end_node(start_node: str, end_node_pattern: str, map_: Map) -> int:
    node = map_.nodes[start_node]
    directions = cycle(map_.directions)
    n = 0
    while not re.match(end_node_pattern, node.name):
        direction = next(directions)
        node = map_.nodes[{"L": node.left, "R": node.right}[direction]]
        n += 1
    return n


def part1(map_: Map) -> None:
    n = steps_until_end_node(start_node="AAA", end_node_pattern="ZZZ", map_=map_)
    print("(Part 1) Steps until last node:", n)


def part2(map_: Map) -> None:
    steps_until_end = (
        steps_until_end_node(start_node=node_name, end_node_pattern="..Z", map_=map_)
        for node_name in map_.nodes
        if node_name.endswith("A")
    )
    least_common_steps_to_end = math.lcm(*steps_until_end)
    print("(Part 2) Steps until first common ending node:", least_common_steps_to_end)


if __name__ == "__main__":
    map_ = read_map("input.txt")
    part1(map_)
    part2(map_)
