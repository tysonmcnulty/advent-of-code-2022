import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Self, Iterator, Callable


def no() -> bool:
    return False


class Keyword(Enum):
    ADDX = "addx"
    NOOP = "noop"


@dataclass
class Register:
    value: int = 1


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


@dataclass
class CPU:
    X: Register = field(default_factory=Register)
    cycle_number: int = 0

    def run(self, program: Program, cycle_interval=None):
        n = 0
        for instruction in program.instructions:
            for _ in range(0, self.get_execution_cycles(instruction)):
                self.cycle_number += 1
                n += 1

                if n == cycle_interval:
                    yield
                    n = 0

            instruction.execute(self.X)

        yield

    @staticmethod
    def get_execution_cycles(instruction) -> int:
        if instruction.keyword == Keyword.NOOP:
            return 1
        elif instruction.keyword == Keyword.ADDX:
            return 2


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
