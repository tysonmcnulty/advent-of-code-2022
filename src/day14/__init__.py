from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from functools import cache, cached_property
from itertools import chain, pairwise, tee
from math import copysign
from typing import Callable, Iterable, Iterator, Optional, Protocol, Self, overload

from src import PathMapping, no

Location = tuple[int, int]
Extent = tuple[Location, Location]


def total_extent(extents: Iterable[Extent]) -> Extent:
    copies = tee(extents, 4)

    min_width = min(map(lambda e: e[0][0], copies[0]))
    min_height = min(map(lambda e: e[0][1], copies[1]))
    max_width = max(map(lambda e: e[1][0], copies[2]))
    max_height = max(map(lambda e: e[1][1], copies[3]))

    return (min_width, min_height), (max_width, max_height)


class Locatable(Protocol):
    location: Location


@dataclass(frozen=True)
class Rock:
    location: Location

    def render(self, canvas):
        canvas.draw("#", self.location)


@dataclass(frozen=True)
class Segment(Sequence[Rock], ABC):
    start: Rock
    end: Rock

    @overload
    def __getitem__(self, i: int) -> Rock:
        ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[Rock]:
        ...

    @abstractmethod
    def __getitem__(self, arg):
        ...

    @staticmethod
    def from_locations(pair: tuple[Location, Location]) -> Self:
        if pair[0][0] == pair[1][0]:
            return HorizontalSegment(*map(Rock, pair))
        if pair[0][1] == pair[1][1]:
            return VerticalSegment(*map(Rock, pair))
        pass

    @cached_property
    def _rocks(self) -> tuple[Rock, ...]:
        rocks = tuple(iter(self))
        return rocks

    @cached_property
    def extent(self) -> Extent:
        extent = min((self.start.location, self.end.location)), max(
            (self.start.location, self.end.location)
        )
        return extent

    def inspect(self, location) -> Optional[Rock]:
        if (
            self.extent[0][0] <= location[0] <= self.extent[1][0]
            and self.extent[0][1] <= location[1] <= self.extent[1][1]
        ):
            return Rock(location)
        else:
            return None


@dataclass(frozen=True)
class VerticalSegment(Segment):
    def __getitem__(self, arg):
        if isinstance(arg, slice):
            return self._rocks[arg]
        elif isinstance(arg, int):
            return Rock(location=self._get_location(arg))
        else:
            raise TypeError(f"no overload available for type: {type(arg)}")

    def __len__(self) -> int:
        return abs(self.end.location[0] - self.start.location[0]) + 1

    @cached_property
    def _direction(self) -> int:
        return int(copysign(1, self.end.location[0] - self.start.location[0]))

    def _get_location(self, index: int) -> Location:
        normalized_index = len(self) + index if index < 0 else index
        if index >= len(self):
            raise IndexError()
        if index < -len(self):
            raise IndexError()

        return (
            self.start.location[0] + normalized_index * self._direction,
            self.start.location[1],
        )


@dataclass(frozen=True)
class HorizontalSegment(Segment):
    def __getitem__(self, arg):
        if isinstance(arg, slice):
            return self._rocks[arg]
        elif isinstance(arg, int):
            return Rock(location=self._get_location(arg))
        else:
            raise TypeError(f"no overload available for type: {type(arg)}")

    def __len__(self) -> int:
        return abs(self.end.location[1] - self.start.location[1]) + 1

    @cached_property
    def _direction(self) -> int:
        return int(copysign(1, self.end.location[1] - self.start.location[1]))

    def _get_location(self, index: int) -> Location:
        normalized_index = len(self) + index if index < 0 else index
        if index >= len(self):
            raise IndexError()
        if index < -len(self):
            raise IndexError()

        return (
            self.start.location[0],
            self.start.location[1] + normalized_index * self._direction,
        )


@dataclass(frozen=True)
class Structure:
    segments: tuple[Segment, ...]

    @cached_property
    def extent(self) -> tuple[Location, Location]:
        extent = total_extent(s.extent for s in self.segments)
        return extent

    @staticmethod
    def from_str(data: str) -> Self:
        locations = map(lambda d: tuple(map(int, d.split(","))), data.split(" -> "))
        return Structure(
            segments=tuple(Segment.from_locations(pair) for pair in pairwise(locations))
        )

    def __iter__(self) -> Iterable[Rock]:
        for s in self.segments:
            for rock in s[:-1]:
                yield rock

        yield self.segments[-1][-1]

    def render(self, canvas):
        for rock in self:
            rock.render(canvas)

    def inspect(self, location) -> Optional[Rock]:
        for s in self.segments:
            if obj := s.inspect(location):
                return obj


class Sand:
    @dataclass(frozen=True)
    class Source:
        location: Location

        def render(self, canvas):
            canvas.draw("+", self.location)

        def generate(self) -> "Sand.Unit":
            return Sand.Unit(location=self.location)

    @dataclass
    class Unit:
        location: Location

        def render(self, canvas):
            canvas.draw("o", self.location)


@dataclass
class SimulationState:
    paths: Mapping[Location, list[Location]]


@dataclass
class Cave:
    structures: frozenset[Structure, ...]
    sand_units: dict[Location, Sand.Unit] = field(default_factory=dict)
    sand_source: Sand.Source = Sand.Source(location=(500, 0))
    _rocks: frozenset[Rock] = field(init=False, compare=False, repr=False)

    def __post_init__(self):
        self._rocks = frozenset(chain.from_iterable(self.structures))

    @property
    def extent(self) -> Extent:
        return Cave._extent(self.structures, self.sand_source)

    def render(self, canvas):
        self.sand_source.render(canvas)
        for rock in self._rocks:
            rock.render(canvas)

        for unit in self.sand_units.values():
            unit.render(canvas)

    def inspect(self, location: Location) -> Optional[Locatable]:
        if Rock(location) in self._rocks:
            return Rock(location)

        if unit := self.sand_units.get(location):
            return unit

    def simulate(
        self, should_stop: Callable[[Self, Optional[Sand.Unit]], bool] = no
    ) -> Iterator[SimulationState]:
        current_unit = self.sand_source.generate()
        previous: dict[Location, Location] = {}
        state = SimulationState(paths=PathMapping(self.sand_source.location, previous))
        empty_locations: list[Location] = [current_unit.location]

        while not should_stop(self, current_unit):
            adjacent_empty_locations = list(
                filter(
                    lambda it: it if not self.inspect(it) else None,
                    possible_next_locations(current_unit),
                )
            )

            empty_locations.extend(reversed(adjacent_empty_locations))
            previous.update(
                {adj: current_unit.location for adj in adjacent_empty_locations}
            )
            if len(adjacent_empty_locations) == 0:
                self.sand_units[current_unit.location] = current_unit
                empty_locations.pop()
                yield state

                if len(empty_locations) == 0:
                    break

                current_unit = self.sand_source.generate()

            current_unit.location = empty_locations[-1]

    @staticmethod
    @cache
    def _extent(structures: frozenset[Structure], sand_source: Sand.Source) -> Extent:
        return total_extent(
            chain(
                (s.extent for s in structures),
                ((sand_source.location, sand_source.location),),
            )
        )


@dataclass
class Canvas:
    extent: Extent
    content: list[list[str]] = field(init=False)

    def __post_init__(self):
        self.content = [
            ["." for _ in range(self.extent[0][0], self.extent[1][0] + 1)]
            for _ in range(self.extent[0][1], self.extent[1][1] + 1)
        ]

    def draw(self, symbol: str, location: Location):
        self.content[location[1] - self.extent[0][1]][
            location[0] - self.extent[0][0]
        ] = symbol

    def print(self, frame: Optional[Extent] = None) -> list[str]:
        _frame: Extent = frame or self.extent
        v_slice = slice(
            _frame[0][1] - self.extent[0][1],
            len(self.content) + _frame[1][1] - self.extent[1][1],
        )
        h_slice = slice(
            _frame[0][0] - self.extent[0][0],
            len(self.content[0]) + _frame[1][0] - self.extent[1][0],
        )
        return [
            "".join(symbol for symbol in row[h_slice]) for row in self.content[v_slice]
        ]


def with_floor(
    structures: frozenset[Structure], horizontal_midpoint=500
) -> frozenset[Structure]:
    structure_extent = total_extent(s.extent for s in structures)
    h = horizontal_midpoint
    d = structure_extent[1][1] + 2
    floor = Segment.from_locations(((h - (d + 1), d), (h + (d + 1), d)))
    return structures | {Structure((floor,))}


def possible_next_locations(unit: Sand.Unit) -> tuple[Location, Location, Location]:
    return (
        (unit.location[0], unit.location[1] + 1),
        (unit.location[0] - 1, unit.location[1] + 1),
        (unit.location[0] + 1, unit.location[1] + 1),
    )


def parse(data: list[str]) -> frozenset[Structure]:
    structures = (Structure.from_str(line.strip()) for line in data)
    return frozenset(structures)
