def move(pos, direction):
    x, y = pos
    return {
        "R": (x + 1, y),
        "U": (x, y + 1),
        "L": (x - 1, y),
        "D": (x, y - 1),
    }[direction]


def move_tail(tail, head):
    x_head, y_head = head
    x_tail, y_tail = tail
    x_dist = x_head - x_tail
    y_dist = y_head - y_tail
    if abs(x_dist) > 1:
        x_tail += sign(x_dist)
        if abs(y_dist) > 0:
            y_tail += sign(y_dist)
    elif abs(y_dist) > 1:
        y_tail += sign(y_dist)
        if abs(x_dist) > 0:
            x_tail += sign(x_dist)
    return x_tail, y_tail


def sign(number):
    return +1 if number >= 0 else -1


def two_node_rope_move(input_path):
    head = (0, 0)
    tail = (0, 0)
    visited = set()

    for line in open(input_path):
        direction, count_str = line.strip().split()
        for _ in range(int(count_str)):
            head = move(pos=head, direction=direction)
            tail = move_tail(tail=tail, head=head)
            visited.add(tail)
    
    return visited


print("Tail visited positions:", len(two_node_rope_move("input.txt")))


# -- Part 2 -- #

def multi_node_rope_move(input_path, n_nodes=10):
    nodes = [(0,0)] * n_nodes
    visited = set()

    for line in open(input_path):
        direction, count_str = line.strip().split()
        for _ in range(int(count_str)):
            nodes[0] = move(pos=nodes[0], direction=direction)
            for i in range(1, len(nodes)):
                nodes[i] = move_tail(tail=nodes[i], head=nodes[i-1])
            visited.add(nodes[-1])

    return visited


def visualize(nodes, visited, size=15):
    """ When in debug mode, call this function in a watch """
    for j in range(size, -size, -1):
        for i in range(-size, size):
            for n, node in enumerate(nodes):
                if (i, j) == node:
                    print(n, end="")
                    break
            else:
                if (i, j) in visited:
                    print("#", end="")
                else:
                    print(".", end="")
        print()


print("Tail visited (10 nodes):", len(multi_node_rope_move("input.txt")))
