from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Pulse(Enum):
    LOW = 1
    HIGH = 2


@dataclass
class Module(ABC):
    name: str
    output: list[str]

    _nlow: int = 0
    _nhigh: int = 0
    _pulse_to_send: Optional[Pulse] = None

    @abstractmethod
    def receive_pulse(self, name: str, pulse: Pulse) -> None:
        raise NotImplemented

    # @abstractmethod
    def send_pulse(self, modules: dict[str, "Module"]) -> None:
        for module in self.output:
            if self._pulse_to_send:
                if self._pulse_to_send == Pulse.HIGH:
                    self._nhigh += 1
                else:
                    self._nlow += 1
                modules[module].receive_pulse(self.name, self._pulse_to_send)
        for module in self.output:
            if modules[module]._pulse_to_send:
                modules[module].send_pulse(modules)


@dataclass
class FlipFlop(Module):
    on: bool = False

    def receive_pulse(self, name: str, pulse: Pulse) -> None:
        if pulse == Pulse.LOW:
            self._pulse_to_send = Pulse.LOW if self.on else Pulse.HIGH
            self.on = not self.on
        else:
            self._pulse_to_send = None


@dataclass
class Conjunction(Module):
    memory: dict[str, Pulse] = field(default_factory=dict)

    def receive_pulse(self, name: str, pulse: Pulse) -> None:
        self.memory[name] = pulse
        if all(pulse == Pulse.HIGH for pulse in self.memory.values()):
            self._pulse_to_send = Pulse.LOW
        else:
            self._pulse_to_send = Pulse.HIGH


@dataclass
class Broadcaster(Module):
    def receive_pulse(self, name: str, pulse: Pulse) -> None:
        self._pulse_to_send = pulse


def read_modules(input_path: str) -> dict[str, Module]:
    with open(input_path) as f:
        modules = {}
        for line in f:
            name, output_str = line.strip().split(" -> ")
            # type_str = name[0] if name != "broadcaster" else "broadcaster"
            output = output_str.split(", ")
            module: Module
            if name == "broadcaster":
                module = Broadcaster(name, output)
            elif name.startswith("%"):
                module = FlipFlop(name[1:], output)
            elif name.startswith("&"):
                module = Conjunction(name[1:], output)
            else:
                raise ValueError("Shouldn't be here")
            modules[module.name] = module
    # Populate input from output
    for name, module in modules.items():
        for out in module.output:
            match modules[out]:
                case Conjunction() as conjunction:
                    conjunction.memory[name] = Pulse.LOW

    return modules


if __name__ == "__main__":
    modules: dict[str, Module] = read_modules("example1.txt")
    modules["broadcaster"].receive_pulse("button", Pulse.LOW)
    modules["broadcaster"].send_pulse(modules)
    print("(Part 1) Pulses", sum(m._nhigh for m in modules.values()))
    print("(Part 1) Pulses", sum(m._nlow for m in modules.values()))
