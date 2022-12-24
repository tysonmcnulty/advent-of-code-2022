import io
import re
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, Optional, Self

import yaml


@dataclass
class Item:
    worry_level: int

    @dataclass(frozen=True)
    class Operation(ABC):
        operator: "Item.Operator" = field(init=False)

        @abstractmethod
        def update(self, item: "Item") -> None:
            ...

        @staticmethod
        def from_str(data: str) -> Self:
            if match_obj := re.match(r"new = old \+ (\d+)", data):
                return Item.Add(int(match_obj.group(1)))
            elif match_obj := re.match(r"new = old \* (\d+)", data):
                return Item.Multiply(int(match_obj.group(1)))
            elif re.match(r"new = old \* old", data):
                return Item.Square()

            raise ValueError(f"no matching operations for string: {data}")

    class Operator(Enum):
        ADD = "add"
        MULTIPLY = "multiply"
        SQUARE = "square"
        FLOOR_DIVIDE = "floor divide"
        MOD = "mod"

    @dataclass(frozen=True)
    class Add(Operation):
        addend: int

        def __post_init__(self):
            object.__setattr__(self, "operator", Item.Operator.ADD)

        def update(self, item: "Item") -> None:
            item.worry_level += self.addend

    @dataclass(frozen=True)
    class Multiply(Operation):
        factor: int

        def __post_init__(self):
            object.__setattr__(self, "operator", Item.Operator.MULTIPLY)

        def update(self, item: "Item") -> None:
            item.worry_level *= self.factor

    @dataclass(frozen=True)
    class Square(Operation):
        def __post_init__(self):
            object.__setattr__(self, "operator", Item.Operator.SQUARE)

        def update(self, item: "Item") -> None:
            item.worry_level **= 2

    @dataclass(frozen=True)
    class FloorDivide(Operation):
        factor: int

        def __post_init__(self):
            object.__setattr__(self, "operator", Item.Operator.FLOOR_DIVIDE)

        def update(self, item: "Item") -> None:
            item.worry_level //= self.factor

    @dataclass(frozen=True)
    class Mod(Operation):
        base: int

        def __post_init__(self):
            object.__setattr__(self, "operator", Item.Operator.MOD)

        def update(self, item: "Item") -> None:
            item.worry_level %= self.base

    @dataclass(frozen=True)
    class DivisibleBy:
        factor: int

        def inspect(self, item) -> bool:
            return item.worry_level % self.factor == 0

        @staticmethod
        def from_str(data: str) -> Self:
            if match_obj := re.match(r"divisible by (\d+)", data):
                return Item.DivisibleBy(int(match_obj.group(1)))

            raise ValueError(f"no match found for string: {data}")


@dataclass
class Monkey:
    number: int
    operation: Item.Operation
    test: Item.DivisibleBy
    if_true: int
    if_false: int
    inspection_count: int = 0
    items: list[Item] = field(default_factory=list)
    game: Optional["KeepAway"] = field(compare=False, repr=False, default=None)

    def throw_items(self):
        while len(self.items) > 0:
            self.throw_next_item()

    def throw_next_item(self):
        item = self.items.pop(0)
        self.update(item)
        result = self.inspect(item)

        if not self.game:
            return

        if catcher := self.game.players.get(self.if_true if result else self.if_false):
            catcher.catch(item)

    def catch(self, item: Item):
        self.items.append(item)

    def update(self, item):
        self.operation.update(item)
        if self.game:
            self.game.operation.update(item)

    def inspect(self, item):
        result = self.test.inspect(item)
        self.inspection_count += 1
        return result


@dataclass(frozen=True)
class KeepAway:
    players: dict[int, Monkey]
    operation: Item.Operation = Item.FloorDivide(3)
    round_results: deque["KeepAway.RoundResult"] = field(default_factory=deque)

    def __post_init__(self):
        for monkey in self.players.values():
            monkey.game = self
            pass

    def play(self, num_rounds=1):
        for _ in range(num_rounds):
            for monkey in self.players.values():
                monkey.throw_items()

            top_two_inspection_counts = sorted(
                list(map(lambda it: it.inspection_count, self.players.values()))
            )[-2:]

            self.round_results.append(
                KeepAway.RoundResult(
                    worry_levels={
                        m.number: list(map(lambda it: it.worry_level, m.items))
                        for m in self.players.values()
                    },
                    monkey_business_level=top_two_inspection_counts[0]
                    * top_two_inspection_counts[1],
                )
            )

    @dataclass(frozen=True)
    class RoundResult:
        worry_levels: dict[int, list[int]]
        monkey_business_level: int


def parse_as_malformed_yaml(lines: list[str]) -> dict[str, dict[str, str]]:
    return yaml.safe_load(
        io.StringIO("".join(map(lambda line: re.sub(r"^ {4}", "  ", line), lines)))
    )


def parse(lines: list[str]) -> Iterator[Monkey]:
    monkey_yaml = parse_as_malformed_yaml(lines)
    for monkey_data in monkey_yaml.items():
        key, value = monkey_data
        monkey_number = int(re.match(r"Monkey (\d+)", key).group(1))

        yield Monkey(
            number=monkey_number,
            operation=Item.Operation.from_str(value["Operation"]),
            test=Item.DivisibleBy.from_str(value["Test"]),
            if_true=int(re.match(r"throw to monkey (\d+)", value["If true"]).group(1)),
            if_false=int(
                re.match(r"throw to monkey (\d+)", value["If false"]).group(1)
            ),
            items=list(
                map(lambda it: Item(int(it)), str(value["Starting items"]).split(","))
            ),
        )
