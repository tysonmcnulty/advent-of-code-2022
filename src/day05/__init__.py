from enum import Enum
from itertools import zip_longest
from re import match
from typing import Self


class Crate:
    def __init__(self, label):
        self.label = label

    def __eq__(self, other):
        if isinstance(other, Crate):
            return self.label == other.label
        else:
            return NotImplemented


StackLabel = str


class Stack:
    def __init__(self, label: StackLabel, crates: list[Crate]):
        self.label = label
        self.crates = crates

    def __eq__(self, other):
        if isinstance(other, Stack):
            return self.crates == other.crates
        else:
            return NotImplemented


class Step:
    def __init__(self, crate_count: int, start: StackLabel, end: StackLabel):
        self.crate_count = crate_count
        self.start = start
        self.end = end

    @staticmethod
    def from_str(data: str) -> Self:
        groups = match(r"move (\d+) from (\d+) to (\d+)", data).groups()
        return Step(int(groups[0]), groups[1], groups[2])

    def __eq__(self, other):
        if isinstance(other, Step):
            return (
                self.crate_count == other.crate_count
                and self.start == other.start
                and self.end == other.end
            )
        else:
            return NotImplemented


class Strategy(Enum):
    CRATE_MOVER_9000 = 9000
    CRATE_MOVER_9001 = 9001


class Ship:
    def __init__(self, stacks: list[Stack]):
        self._stacks = dict([(s.label, s) for s in stacks])

    def __eq__(self, other):
        if isinstance(other, Ship):
            return self.stacks == other.stacks
        else:
            return NotImplemented

    @property
    def stacks(self):
        return list(self._stacks.values())

    def run_crane(self, steps: list[Step], strategy=Strategy.CRATE_MOVER_9000):
        for step in steps:
            start_crates = self._stacks[step.start].crates
            end_crates = self._stacks[step.end].crates
            n = step.crate_count
            crates = start_crates[-n:]
            del start_crates[-n:]
            match strategy:
                case Strategy.CRATE_MOVER_9000:
                    end_crates.extend(reversed(crates))
                case Strategy.CRATE_MOVER_9001:
                    end_crates.extend(crates)


def load_data(data_file: str) -> list[str]:
    with open(data_file) as data:
        return [*data]


def parse(data: list[str]) -> tuple[Ship, list[Step]]:
    stack_row_data = []
    data_iter = iter(data)

    for line in data_iter:
        if line.isspace():
            break
        else:
            stack_row_data.append(
                [line[i : min(i + 4, len(line))] for i in range(0, len(line), 4)]
            )

    steps = [Step.from_str(line.strip()) for line in data_iter]

    stacks = []
    for stack_data in zip_longest(*reversed(stack_row_data)):
        stack_args = [
            d.strip() for d in stack_data if d is not None and not d.isspace()
        ]
        stacks.append(Stack(stack_args[0], [Crate(lbl[1]) for lbl in stack_args[1:]]))

    return (Ship(stacks), steps)


def load(data_file: str) -> tuple[Ship, list[Step]]:
    return parse(load_data(data_file))
