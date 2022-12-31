from dataclasses import dataclass
import re

from tqdm import tqdm


@dataclass
class Valve:
    code: str
    rate: int
    adjacent: list["Valve"]
    is_open: bool = False

    def __repr__(self):
        adjacent_codes = [adj.code for adj in self.adjacent]
        return f"Valve({self.code}, {self.rate}, {adjacent_codes})"


def parse_valves(path: str) -> dict[str, Valve]:
    valves = {}
    for line in open(path):
        line = line.strip()
        code = line[len("Valve ") : line.find(" has")]
        rate = int(line[line.find("rate=") + 5 : line.find(";")])
        adjacent_codes = re.findall(r"[A-Z]+", line[line.find(";") :])
        valves[code] = Valve(code, rate, adjacent_codes)
    for valve in valves.values():
        valve.adjacent = list(map(valves.get, valve.adjacent))  # type: ignore
    return valves


def pressure_released_in_minute(valves: dict[str, Valve]) -> int:
    """Get pressure released on this minute."""
    return sum(valve.rate for valve in valves.values() if valve.is_open)


def do_action(valve: Valve) -> Valve:
    cur_valve = valve
    if valve.rate > 0 and not valve.is_open:
        valve.is_open = True
    else:
        cur_valve = valve.adjacent[0]
    return cur_valve


def pressure_released(valves: dict[str, Valve], starting_valve: str, minutes: int):
    """Get pressure released over minutes."""
    pressure_released = 0
    cur_valve = valves[starting_valve]
    for _ in tqdm(range(minutes)):
        pressure_released += pressure_released_in_minute(valves)
        cur_valve = do_action(cur_valve)
    return pressure_released


def part1(valves: dict[str, Valve]):
    minutes = 30
    starting_valve = "AA"
    amount_press_released = pressure_released(
        valves, starting_valve=starting_valve, minutes=minutes
    )
    print(
        f"Amount of pressure released during {minutes} minutes:", amount_press_released
    )


if __name__ == "__main__":
    input_path = "sample_input.txt"
    valves = parse_valves(input_path)
    part1(valves)
