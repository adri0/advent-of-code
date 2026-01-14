from collections import deque
from typing import NamedTuple


class Node(NamedTuple):
    label: str
    next: list["Node"]


with open("input.txt") as f:
    network: dict[str, Node] = {}
    for line in f:
        cur, *next_nodes = line.split()
        cur = cur[:-1]
        node = network.get(cur, Node(cur, []))
        for nxt in next_nodes:
            nxt_node = network.get(nxt, Node(nxt, []))
            node.next.append(nxt_node)
            network[nxt] = nxt_node
        network[node.label] = node

queue = deque([network["you"]])

paths = 0
while queue:
    node = queue.popleft()
    if node.next:
        queue += node.next
    else:
        assert node.label == "out"
        paths += 1

print(f"{paths=}")
