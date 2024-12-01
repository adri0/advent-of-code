from collections import Counter


def read_input(path: str) -> tuple[list[int], list[int]]:
    list1 = []
    list2 = []
    with open(path, "r") as f:
        for line in f:
            n1, n2 = line.split()
            list1.append(int(n1))
            list2.append(int(n2))
    return list1, list2


def part1(list1: list[int], list2: list[int]) -> int:
    list1_sort = sorted(list1)
    list2_sort = sorted(list2)
    total_distance = sum(abs(ele2 - ele1) for ele1, ele2 in zip(list1_sort, list2_sort))
    return total_distance


def part2(list1: list[int], list2: list[int]) -> int:
    list2_counter = Counter(list2)
    similarity = sum(ele1 * list2_counter[ele1] for ele1 in list1)
    return similarity


if __name__ == "__main__":
    list1, list2 = read_input("01/input.txt")

    total_distance = part1(list1, list2)
    print(f"(Part 1) total_distance = {total_distance}")

    similarity = part2(list1, list2)
    print(f"(Part 2) similartiy = {similarity}")
