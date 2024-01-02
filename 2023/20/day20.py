import math
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple, cast


class Intensity(Enum):
    LOW = 0
    HIGH = 1


class Pulse(NamedTuple):
    source: str
    target: str
    intensity: Intensity


@dataclass
class Module(ABC):
    name: str
    out_connections: list[str]

    @abstractmethod
    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        raise NotImplemented

    def generate_pulses(self, intensity: Intensity) -> list[Pulse]:
        return [
            Pulse(source=self.name, target=module, intensity=intensity)
            for module in self.out_connections
        ]


@dataclass
class FlipFlop(Module):
    on: bool = False

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.intensity == Intensity.HIGH:
            return []
        else:
            out_intensity = Intensity.LOW if self.on else Intensity.HIGH
            self.on = not self.on
            return self.generate_pulses(out_intensity)


class Conjunction(Module):
    def __init__(self, name: str, out_connections: list[str]) -> None:
        super().__init__(name, out_connections)
        self.memory: dict[str, Intensity] = {}
        self.prev_memory: dict[str, Intensity] = {}

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.prev_memory[pulse.source] = self.memory[pulse.source]
        self.memory[pulse.source] = pulse.intensity
        out_intensity = (
            Intensity.LOW
            if all(intensity == Intensity.HIGH for intensity in self.memory.values())
            else Intensity.HIGH
        )
        return self.generate_pulses(out_intensity)


class Broadcaster(Module):
    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        return self.generate_pulses(pulse.intensity)


class Output(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name, out_connections=[])

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        return []


def parse_module(input_line: str) -> Module:
    name, connect_str = input_line.strip().split(" -> ")
    out_modules = connect_str.split(", ")
    module: Module
    if name == "broadcaster":
        module = Broadcaster(name, out_modules)
    elif name.startswith("%"):
        module = FlipFlop(name[1:], out_modules)
    elif name.startswith("&"):
        module = Conjunction(name[1:], out_modules)
    else:
        raise ValueError("Shouldn't be here")
    return module


def read_modules(input_path: str) -> dict[str, Module]:
    with open(input_path) as f:
        modules = {module.name: module for module in map(parse_module, f)}

    # Identify output modules and populate memory for conjunctions
    out_modules = {}
    for module in modules.values():
        for out in module.out_connections:
            if out not in modules and out not in out_modules:
                out_modules[out] = Output(name=out)
            elif isinstance(modules[out], Conjunction):
                cast(Conjunction, modules[out]).memory[module.name] = Intensity.LOW
    modules.update(out_modules)

    return modules


def part1(modules: dict[str, Module]) -> None:
    lows = highs = 0
    for _ in range(1000):
        pulses = [Pulse(source="button", target="broadcaster", intensity=Intensity.LOW)]
        while pulses:
            pulse = pulses.pop()
            out_pulses = modules[pulse.target].receive_pulse(pulse)
            pulses = out_pulses + pulses
            highs += int(pulse.intensity == Intensity.HIGH)
            lows += int(pulse.intensity == Intensity.LOW)

    print("(Part 1) Result:", lows * highs)


def part2(modules: dict[str, Module]) -> None:
    n_button_press = 0
    pulse_found = False
    kh = cast(Conjunction, modules["kh"])
    pulses_per_kh_con = {mod: defaultdict(list) for mod in kh.memory}

    while not pulse_found:
        n_button_press += 1
        pulses = [Pulse(source="button", target="broadcaster", intensity=Intensity.LOW)]
        n_pulses = 0
        while pulses:
            n_pulses += 1
            pulse = pulses.pop()
            if pulse.target == "rx" and pulse.intensity == Intensity.LOW:
                pulse_found = True
                break
            out_pulses = modules[pulse.target].receive_pulse(pulse)
            pulses = out_pulses + pulses

            # if pulse.target == "rx":
            #     for mod, i in kh.memory.items():
            #         if i == Intensity.HIGH:
            #             pulses_per_kh_con[mod][n_button_press].append(n_pulses)

        for mod, i in kh.memory.items():
            if i == Intensity.HIGH:
                print("npress", n_button_press, kh)
        # if len(pulses_per_kh_con[]):
        #     print(pulses_per_kh_con)
        #     # print(pulses_per_press)
        #     pulse_found = True
        #     break
        #     pulses_per_kh_con[pulse.source].append(n_pulses)
        # if len(pulses_per_kh_con["hz"]) == 8:

    lcm = math.lcm(*pulses_per_kh_con.values())
    print("lcm:", lcm)
    print("per button", (lcm // 60) // 42)

    print("(Part 2) Result:", n_button_press)


if __name__ == "__main__":
    # modules = read_modules("input.txt")
    # part1(modules)
    modules = read_modules("input.txt")
    part2(modules)
