from functools import reduce

trees_mat = [list(map(int, line.strip())) for line in open("input.txt")]


def tree_is_visible(trees_mat, i_tree, j_tree):
    inv_ax = 0
    tree_height = trees_mat[j_tree][i_tree]

    for i in range(0, i_tree):
        if trees_mat[j_tree][i] >= tree_height:
            inv_ax += 1
            break

    for i in range(i_tree + 1, len(trees_mat[0])):
        if trees_mat[j_tree][i] >= tree_height:
            inv_ax += 1
            break

    for j in range(0, j_tree):
        if trees_mat[j][i_tree] >= tree_height:
            inv_ax += 1
            break

    for j in range(j_tree + 1, len(trees_mat)):
        if trees_mat[j][i_tree] >= tree_height:
            inv_ax += 1
            break
        
    return inv_ax < 4
    

def count_visible_trees(trees_mat: list[list[int]]) -> int:
    n_visible = 0
    for i in range(1, len(trees_mat[0]) - 1):
        for j in range(1, len(trees_mat) - 1):
            if tree_is_visible(trees_mat, i, j):
                n_visible += 1
    n_visible += 2 * len(trees_mat[0])
    n_visible += 2 * (len(trees_mat) - 2)
    return n_visible


print("Visible:", count_visible_trees(trees_mat))


# -- Part 2 -- #

def scenic_score(trees_mat, i_tree, j_tree):
    scenic_factors = [0, 0, 0, 0]
    tree_height = trees_mat[j_tree][i_tree]

    for i in range(i_tree + 1, len(trees_mat[0])):  # Go east
        scenic_factors[0] += 1
        if trees_mat[j_tree][i] >= tree_height:
            break

    for i in range(i_tree - 1, -1, -1):  # Go wast
        scenic_factors[1] += 1
        if trees_mat[j_tree][i] >= tree_height:
            break

    for j in range(j_tree - 1, -1, -1):  # Go north
        scenic_factors[2] += 1
        if trees_mat[j][i_tree] >= tree_height:
            break

    for j in range(j_tree + 1, len(trees_mat)):  # Go south
        scenic_factors[3] += 1
        if trees_mat[j][i_tree] >= tree_height:
            break
        
    return reduce(lambda a, b: a * b, scenic_factors)


def max_scenic_score(trees_mat: list[list[int]]) -> int:
    max_score = 0
    for i in range(len(trees_mat[0])):
        for j in range(len(trees_mat)):
            max_score = max(scenic_score(trees_mat, i, j), max_score)
    return max_score


print("Max scenic score:", max_scenic_score(trees_mat))