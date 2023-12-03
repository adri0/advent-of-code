import re
from functools import partial, reduce
from typing import Iterable, NamedTuple


class Coord(NamedTuple):
    x: int
    y: int


class Element(NamedTuple):
    content: str | int
    coords: tuple


Schematic = dict[Coord, Element]


def read_schematic_from_file(path: str) -> Schematic:
    schematic = {}
    with open(path, "r") as f:
        for i, line in enumerate(f):
            coord_map = read_coords_from_line(line, i)
            schematic.update(coord_map)
    return schematic


def read_coords_from_line(line: str, line_number: int) -> Schematic:
    """Line example: 467..114.."""
    coords = {}
    # Match sequence of digits or single chars that aren't digit nor dot.
    for match in re.finditer(r"\d+|[^.\d]{1}", line.strip()):
        content = match.group()
        element = Element(
            content=int(content) if content.isnumeric() else content,
            coords=tuple(Coord(x=pos, y=line_number) for pos in range(*match.span())),
        )
        coords.update({coord: element for coord in element.coords})
    return coords


def filter_symbols(elements: Iterable[Element]) -> list[Element]:
    return [element for element in elements if isinstance(element.content, str)]


def get_adjacent_number_elements(symbol: Element, schematic: Schematic) -> set[Element]:
    symbol_coord = symbol.coords[0]
    adjacent_coords = [
        Coord(symbol_coord.x + i, symbol_coord.y + j)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        if not (i == j == 0)
    ]

    adjacent = set()
    for coord in adjacent_coords:
        element = schematic.get(coord)
        if element and isinstance(element.content, int):
            adjacent.add(element)

    return adjacent


def get_gears_ratios(
    symbols: list[Element], schematic: Schematic
) -> list[tuple[Element, int]]:
    gears_ratios = []
    for element in symbols:
        adjacent_elements = get_adjacent_number_elements(element, schematic)
        if len(adjacent_elements) == 2:
            adj1, adj2 = adjacent_elements
            gears_ratios.append((element, int(adj1.content) * int(adj2.content)))
    return gears_ratios


def part1(schematic: Schematic, symbols: list[Element]) -> None:
    part_numbers = reduce(
        set.union,
        map(partial(get_adjacent_number_elements, schematic=schematic), symbols),
    )
    part_numbers_sum = sum(int(element.content) for element in part_numbers)
    print("Sum of the part numbers:", part_numbers_sum)


def part2(schematic: Schematic, symbols: list[Element]) -> None:
    gears_ratios = get_gears_ratios(symbols, schematic)
    gear_ratio_sum = sum(ratio for gear, ratio in gears_ratios)
    print("Sum of gears ratios:", gear_ratio_sum)


if __name__ == "__main__":
    schematic = read_schematic_from_file("input.txt")
    symbols = filter_symbols(schematic.values())
    part1(schematic, symbols)
    part2(schematic, symbols)
