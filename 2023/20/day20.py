from abc import ABC, abstractmethod
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


@dataclass
class Conjunction(Module):
    memory: dict[str, Intensity] = field(default_factory=dict)

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
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


if __name__ == "__main__":
    modules = read_modules("input.txt")
    part1(modules)
