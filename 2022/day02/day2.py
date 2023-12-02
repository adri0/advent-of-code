input_list = [line.strip().split() for line in open("input.txt")]

ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"

WIN = "win"
DRAW = "draw"
LOSE = "lose"

code_to_sign = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}


def sign_to_points(sign):
    return {ROCK: 1, PAPER: 2, SCISSORS: 3}[sign]


def result_to_points(game_result):
    return {WIN: 6, DRAW: 3, LOSE: 0}[game_result]


def get_game_result(opponent, mine):
    if mine == opponent:
        return DRAW
    elif (
        (mine == PAPER and opponent == ROCK)
        or (mine == SCISSORS and opponent == PAPER)
        or (mine == ROCK and opponent == SCISSORS)
    ):
        return WIN
    else:
        return LOSE


def points_obtained(opponent, mine):
    opponent_sign = code_to_sign[opponent]
    my_sign = code_to_sign[mine]
    result = get_game_result(opponent_sign, my_sign)
    return sign_to_points(my_sign) + result_to_points(result)


result1 = sum(points_obtained(codes[0], codes[1]) for codes in input_list)
print(result1)


# -- Part 2 -- #

ROCK = "A"
PAPER = "B"
SCISSORS = "C"

LOSE = "X"
DRAW = "Y"
WIN = "Z"


def sign_given_result(opponent_sign, game_result):
    for my_sign in (ROCK, PAPER, SCISSORS):
        if get_game_result(opponent_sign, my_sign) == game_result:
            return my_sign


def points_obtained(opponent_sign, game_result):
    my_sign = sign_given_result(opponent_sign, game_result)
    return sign_to_points(my_sign) + result_to_points(game_result)


result2 = sum(points_obtained(codes[0], codes[1]) for codes in input_list)
print(result2)
