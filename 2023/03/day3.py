import re
from functools import partial, reduce
from typing import NamedTuple


class Coord(NamedTuple):
    x: int
    y: int


class Element(NamedTuple):
    content: str
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
        element = Element(
            content=match.group(),
            coords=tuple(Coord(x=pos, y=line_number) for pos in range(*match.span())),
        )
        coords.update({coord: element for coord in element.coords})
    return coords


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
        if element and element.content.isnumeric():
            adjacent.add(element)

    return adjacent


def part1(schematic: Schematic, symbols: list[Element]) -> None:
    part_numbers = reduce(
        set.union,
        map(partial(get_adjacent_number_elements, schematic=schematic), symbols),
    )
    part_numbers_sum = sum(int(element.content) for element in part_numbers)
    print("Sum of the part numbers:", part_numbers_sum)


def part2(schematic: Schematic, symbols: list[Element]) -> None:
    gears_ratios = []
    for element in symbols:
        adjacent_elements = get_adjacent_number_elements(element, schematic)
        if len(adjacent_elements) == 2:
            adj1, adj2 = adjacent_elements
            gears_ratios.append(int(adj1.content) * int(adj2.content))
    print("Sum of gears ratios:", sum(gears_ratios))


if __name__ == "__main__":
    schematic = read_schematic_from_file("example.txt")
    symbols = [elem for elem in schematic.values() if not elem.content.isnumeric()]
    part1(schematic, symbols)
    part2(schematic, symbols)
