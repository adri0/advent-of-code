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


def count_paths(start: str, end: str, network: dict[str, Node]) -> int:
    queue = deque([network[start]])
    n_paths = 0
    i = 0
    while queue:
        node = queue.popleft()
        if node.label == end:
            n_paths += 1
            i = 0
        else:
            queue += node.next
        if i > 500_000_000:
            break
        i += 1
    print(f"({start}, {end})={n_paths}")
    return n_paths


n_paths = (
    count_paths("dac", "out", network)
    * count_paths("fft", "dac", network)
    * count_paths("svr", "fft", network)
) + (
    count_paths("fft", "out", network)
    * count_paths("dac", "fft", network)
    * count_paths("svr", "dac", network)
)

print(f"{n_paths=}")
