from functools import reduce

input_list = [line.strip() for line in open("input.txt")]

LETTERS_LOWER = "abcdefghijklmnopqrstuvwxyz"
ALL_LETTERS = LETTERS_LOWER + LETTERS_LOWER.upper()


def priority(item):
    return ALL_LETTERS.find(item) + 1


def find_dup_item(rucksack):
    comp_1 = rucksack[:len(rucksack)//2]
    comp_2 = rucksack[len(rucksack)//2:]
    return set(comp_1).intersection(set(comp_2)).pop()


result1 = sum([priority(find_dup_item(racksack)) for racksack in input_list])
print(result1)


# -- Part 2 -- #
groups = [input_list[i:i+3] for i in range(0, len(input_list), 3)]

def find_common_item(rucksacks):
    return reduce(lambda a, b: a.intersection(b), map(set, rucksacks)).pop()

result2 = sum(map(priority, map(find_common_item, groups)))
print(result2)