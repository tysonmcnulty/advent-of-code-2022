import re
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Iterator, Self, TypedDict

from src import Receiver


class Keyword(Enum):
    ADDX = "addx"
    NOOP = "noop"


@dataclass
class Register:
    value: int = 1


@dataclass
class Sprite:
    center_position: int = 0
    width: int = 1


@dataclass
class Instruction(ABC):
    keyword: Keyword = field(init=False)
    arguments: list[str] = field(default_factory=list)

    @staticmethod
    def from_str(data: str) -> Self:
        keyword_value, argument_values = re.match(r"(\w+)\s?(.*)", data).group(1, 2)
        keyword = Keyword(keyword_value)
        arguments = (argument_values or "").split(" ")
        if keyword == Keyword.NOOP:
            return Noop()
        elif keyword == Keyword.ADDX:
            return Addx(arguments)
        else:
            raise ValueError()

    @abstractmethod
    def execute(self, register: Register) -> None:
        pass


@dataclass
class Program:
    instructions: Iterator[Instruction]


RegisterState = TypedDict("RegisterState", {"value": int})
CPUState = TypedDict("CPUState", {"X": RegisterState, "cycle_number": int})


@dataclass
class CPU:
    X: Register = field(default_factory=Register)
    cycle_number: int = 0
    receivers: dict[str, Receiver[CPUState]] = field(default_factory=dict)

    def run(self, program: Program):
        for instruction in program.instructions:
            for _ in range(0, self.get_execution_cycles(instruction)):
                self.tick()

            instruction.execute(self.X)

    def tick(self):
        self.cycle_number += 1
        state = asdict(self)
        for it in self.receivers.items():
            it[1].receive(state)

    @staticmethod
    def get_execution_cycles(instruction: Instruction) -> int:
        if instruction.keyword == Keyword.NOOP:
            return 1
        elif instruction.keyword == Keyword.ADDX:
            return 2


class Pixel(Enum):
    DARK = "."
    LIT = "#"


@dataclass
class CRT:
    width: int = 40
    height: int = 6
    pixels: list[list[Pixel]] = field(init=False)
    sprite: Sprite = field(default_factory=Sprite)

    def __post_init__(self):
        self.pixels = [
            [Pixel.DARK for _ in range(self.width)] for _ in range(self.height)
        ]

    def receive(self, cpu_state: CPUState):
        self.sprite.center_position = cpu_state["X"]["value"]
        current_row_index, current_pixel_index = divmod(
            (cpu_state["cycle_number"] - 1), self.width
        )
        current_pixel_value = (
            Pixel.LIT
            if abs(self.sprite.center_position - current_pixel_index)
            <= self.sprite.width
            else Pixel.DARK
        )
        self.pixels[current_row_index][current_pixel_index] = current_pixel_value

    def render(self) -> list[str]:
        return ["".join(p.value for p in row) for row in self.pixels]


@dataclass
class Device:
    cpu: CPU = field(default_factory=CPU)
    crt: CRT = field(default_factory=CRT)

    def __post_init__(self):
        self.install("crt", self.crt)

    def install(self, name: str, receiver: Receiver[CPUState]):
        self.cpu.receivers[name] = receiver

    def run(self, program: Program):
        self.cpu.run(program)


@dataclass
class Noop(Instruction):
    def __post_init__(self):
        object.__setattr__(self, "keyword", Keyword.NOOP)

    def execute(self, register: Register) -> None:
        pass


@dataclass
class Addx(Instruction):
    def __post_init__(self):
        object.__setattr__(self, "keyword", Keyword.ADDX)

    def execute(self, register: Register) -> None:
        register.value += int(self.arguments[0])
        pass


def parse(data: list[str]) -> list[Instruction]:
    return [Instruction.from_str(d.strip()) for d in data]
