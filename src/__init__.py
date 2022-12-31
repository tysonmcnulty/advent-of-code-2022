from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Optional, Protocol, TypeVar


def load_data(data_file: Path) -> list[str]:
    with open(data_file) as data:
        return [*data]


T = TypeVar("T")


class Receiver(Protocol[T]):
    def receive(self, value: T) -> None:
        ...


def yes(*_args: Any) -> bool:
    return True


def no(*_args: Any) -> bool:
    return False


@dataclass
class PathMapping(Mapping[T, Optional[list[T]]]):
    start: T
    previous: dict[T, T]

    def __getitem__(self, key: tuple[T]) -> Optional[list[T]]:
        path = []
        current = key
        while not current == self.start:
            path.append(current)
            current = self.previous[current]

        path.append(self.start)
        return path

    def __len__(self) -> int:
        return len(self.previous)

    def __iter__(self) -> Iterator[tuple[int, int]]:
        return iter(self.previous)
