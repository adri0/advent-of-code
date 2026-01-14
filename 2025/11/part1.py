from collections import deque
from typing import NamedTuple


class Node(NamedTuple):
    label: str
    next: list["Node"]


with open("input.txt") as f:
    network: dict[str, Node] = {}
    for line in f:
        origin_label, *output = line.split()
        origin_label = origin_label[:-1]
        origin = network.get(origin_label, Node(origin_label, []))
        for out in output:
            out_node = network.get(out, Node(out, []))
            origin.next.append(out_node)
            network[out] = out_node
        network[origin.label] = origin

queue: deque[Node] = deque()
queue.append(network["you"])

paths = 0
while queue:
    node = queue.pop()
    if node.next:
        for n in node.next:
            queue.append(n)
    else:
        assert node.label == "out"
        paths += 1

print(f"{paths=}")
