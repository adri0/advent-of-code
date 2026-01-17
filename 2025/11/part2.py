from functools import lru_cache

with open("input.txt") as f:
    network: dict[str, list[str]] = {}
    for line in f:
        cur, *next_nodes = line.split()
        network[cur[:-1]] = next_nodes


@lru_cache(maxsize=None)
def count_paths(node: str, dac: bool, fft: bool) -> int:
    if node == "dac":
        dac = True
    if node == "fft":
        fft = True

    if not network.get(node):
        assert node == "out"
        return int(dac and fft)
    else:
        return sum(count_paths(next, dac, fft) for next in network[node])


n_paths = count_paths("svr", False, False)

print(f"{n_paths=}")
