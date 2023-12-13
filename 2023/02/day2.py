import re
from typing import NamedTuple


class CubeSet(NamedTuple):
    red: int
    green: int
    blue: int


class Game(NamedTuple):
    id: int
    cube_sets: list[CubeSet]


def read_games_from_input(path_input: str) -> list[Game]:
    with open(path_input, "r") as f:
        return list(map(parse_game, f))


def parse_game(line: str) -> Game:
    game_id = int(line[len("Game ") : line.find(":")])
    cube_set_strings = line[line.find(":") :].split(";")
    return Game(game_id, list(map(parse_cube_set, cube_set_strings)))


def parse_cube_set(cs_string: str) -> CubeSet:
    red = colour_quantity(cs_string, "red")
    green = colour_quantity(cs_string, "green")
    blue = colour_quantity(cs_string, "blue")
    return CubeSet(red, green, blue)


def colour_quantity(cs_string: str, colour: str) -> int:
    matches = re.findall(rf"(\d+) {colour}", cs_string)
    return int(matches[0]) if matches else 0


def filter_possible_games(games: list[Game]) -> list[Game]:
    return [game for game in games if all(map(cube_set_possible, game.cube_sets))]


BIGGEST_CUBE_SET = CubeSet(red=12, green=13, blue=14)


def cube_set_possible(cube_set: CubeSet) -> bool:
    return (
        cube_set.red <= BIGGEST_CUBE_SET.red
        and cube_set.green <= BIGGEST_CUBE_SET.green
        and cube_set.blue <= BIGGEST_CUBE_SET.blue
    )


def minimal_cube_set(game: Game) -> CubeSet:
    red = max(cs.red for cs in game.cube_sets)
    green = max(cs.green for cs in game.cube_sets)
    blue = max(cs.blue for cs in game.cube_sets)
    return CubeSet(red, green, blue)


def part1(games: list[Game]) -> None:
    possible_games = filter_possible_games(games)
    sum_of_ids = sum(game.id for game in possible_games)
    print("Sum of IDs of all possible games:", sum_of_ids)


def part2(games: list[Game]) -> None:
    min_cube_set_per_game = map(minimal_cube_set, games)
    cube_set_powers = (cs.red * cs.green * cs.blue for cs in min_cube_set_per_game)
    print("Cube set power sum:", sum(cube_set_powers))


if __name__ == "__main__":
    games = read_games_from_input("input.txt")
    part1(games)
    part2(games)
