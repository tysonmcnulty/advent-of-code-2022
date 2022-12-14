from dataclasses import InitVar, dataclass, field
from enum import Enum
from re import match
from typing import Iterator, Optional, Self


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)

    @staticmethod
    def from_str(value: str) -> Self:
        if value == "U":
            return Direction.UP
        elif value == "D":
            return Direction.DOWN
        elif value == "R":
            return Direction.RIGHT
        elif value == "L":
            return Direction.LEFT
        else:
            raise ValueError()


@dataclass(frozen=True)
class Move:
    direction: Direction


@dataclass(eq=True)
class Segment:
    position: tuple[int, int] = (0, 0)
    linked_to: Optional[Self] = None

    def __iter__(self):
        yield self
        if self.linked_to:
            yield from self.linked_to

    def move_to(self, position: tuple[int, int]):
        self.position = position
        if self.linked_to:
            delta = (
                self.position[0] - self.linked_to.position[0],
                self.position[1] - self.linked_to.position[1],
            )
            if abs(delta[0]) == 2 and abs(delta[1]) == 2:
                self.linked_to.move_to(
                    (
                        int((self.linked_to.position[0] + self.position[0]) / 2),
                        int((self.linked_to.position[1] + self.position[1]) / 2),
                    )
                )
            elif abs(delta[0]) == 2:
                self.linked_to.move_to(
                    (
                        int((self.linked_to.position[0] + self.position[0]) / 2),
                        self.position[1],
                    )
                )
            elif abs(delta[1]) == 2:
                self.linked_to.move_to(
                    (
                        self.position[0],
                        int((self.linked_to.position[1] + self.position[1]) / 2),
                    )
                )


@dataclass(eq=True)
class Rope:
    head: Segment = field(init=False)
    num_segments: InitVar[int] = 2

    def __post_init__(self, num_segments):
        if num_segments < 1:
            raise ValueError()

        current_segment = Segment()
        for _ in range(num_segments - 1):
            next_segment = Segment()
            next_segment.linked_to = current_segment
            current_segment = next_segment

        self.head = current_segment

    @property
    def segments(self) -> Iterator[Segment]:
        yield from self.head

    @property
    def tail(self) -> Segment:
        return [*self.segments][-1]

    def move(self, move: Move):
        self.head.move_to(
            (
                self.head.position[0] + move.direction.value[0],
                self.head.position[1] + move.direction.value[1],
            )
        )


def link(segments: list[Segment]) -> list[Segment]:
    segments_iter = reversed(segments)
    current_segment = next(segments_iter)

    for next_segment in segments_iter:
        next_segment.linked_to = current_segment
        current_segment = next_segment

    return segments


def record_tail_positions(rope: Rope, moves: Iterator[Move]) -> set[tuple[int, int]]:
    visited_positions = set([])
    tail = rope.tail
    for move in moves:
        rope.move(move)
        visited_positions.add(tail.position)

    return visited_positions


def parse(data: list[str]) -> Iterator[Move]:
    for line in data:
        where, how_many = match(r"([UDLR]) (\d+)", line).group(1, 2)
        for _ in range(int(how_many)):
            yield Move(Direction.from_str(where))
