from collections import deque
from collections.abc import Mapping
from dataclasses import InitVar, dataclass, field
from enum import Enum
from functools import cache, cached_property
from typing import Callable, ClassVar, Iterator, Optional, Self

from src import no


@dataclass
class Square:
    elevation: str
    position: tuple[int, int]
    heightmap: "Heightmap" = field(compare=False, repr=False)

    _elevation_keys: ClassVar[dict[str, int]] = {"S": 0, "E": 25} | {
        x[1]: x[0] for x in enumerate("abcdefghijklmnopqrstuvwxyz")
    }

    @property
    def neighbors(self) -> set[Self]:
        return set()

    @property
    def elevation_value(self):
        return self._elevation_keys[self.elevation]


@dataclass
class Heightmap:
    elevations: InitVar[list[str]]
    squares: list[list[Square]] = field(init=False)

    def __post_init__(self, elevations: list[str]):
        self.squares = [
            list(map(lambda j: Square(j[1], (i[0], j[0]), self), enumerate(i[1])))
            for i in enumerate(elevations)
        ]

    @cached_property
    def current_location(self) -> Optional[Square]:
        for row in self.squares:
            for square in row:
                if square.elevation == "S":
                    return square

        return None

    @cached_property
    def best_signal_location(self) -> Optional[Square]:
        for row in self.squares:
            for square in row:
                if square.elevation == "E":
                    return square

        return None

    def square_at(self, position: tuple[int, int]) -> Optional[Square]:
        if position[0] < 0 or position[1] < 0:
            return None
        try:
            return self.squares[position[0]][position[1]]
        except IndexError:
            return None

    def neighbors_of(self, square: Square) -> Iterator[Square]:
        row, col = square.position
        return filter(
            lambda x: x is not None,
            [
                self.square_at((row + 1, col)),
                self.square_at((row - 1, col)),
                self.square_at((row, col + 1)),
                self.square_at((row, col - 1)),
            ],
        )


@dataclass(frozen=True)
class PathMapping(Mapping[tuple[int, int], Optional[list[tuple[int, int]]]]):
    _start_position: tuple[int, int]
    _previous_positions: dict[tuple[int, int], tuple[int, int]]

    def __getitem__(self, key: tuple[int, int]) -> Optional[list[tuple[int, int]]]:
        path = []
        current = key
        try:
            while not current == self._start_position:
                path.append(current)
                current = self._previous_positions[current]
        except KeyError:
            return None

        path.append(self._start_position)
        return path

    def __len__(self) -> int:
        return len(self._previous_positions)

    def __iter__(self) -> Iterator[tuple[int, int]]:
        return iter(self._previous_positions)


@dataclass
class Hiker:
    heightmap: Heightmap
    search_mode: "Hiker.SearchMode"
    location: Square = field(init=False)

    def __post_init__(self):
        self.location = self.heightmap.current_location

    @property
    def accessible_squares(self) -> Iterator[Square]:
        neighbors = self.heightmap.neighbors_of(self.location)
        if self.search_mode == Hiker.SearchMode.FORWARD:
            return filter(
                lambda sq: self.location.elevation_value + 1 >= sq.elevation_value,
                neighbors,
            )
        else:
            return filter(
                lambda sq: sq.elevation_value + 1 >= self.location.elevation_value,
                neighbors,
            )

    def navigate(self, should_stop: Callable[[Square], bool] = no):
        start: tuple[int, int] = self.location.position
        previous: dict[tuple[int, int], tuple[int, int]] = {}

        discovered: set[tuple[int, int]] = set()
        unexplored: deque[Square] = deque([self.location])

        while len(unexplored) > 0:
            self.location = unexplored.popleft()
            if should_stop(self.location):
                break

            newly_discovered = list(
                sq for sq in self.accessible_squares if sq.position not in discovered
            )
            unexplored.extend(newly_discovered)
            previous.update(
                {sq.position: self.location.position for sq in newly_discovered}
            )
            discovered.update(sq.position for sq in newly_discovered)

        return PathMapping(start, previous)

    class SearchMode(Enum):
        FORWARD = "forward"
        REVERSE = "reverse"


def parse(lines: list[str]) -> Hiker:
    return Hiker(
        heightmap=Heightmap([line.strip() for line in lines]),
        search_mode=Hiker.SearchMode.FORWARD,
    )
