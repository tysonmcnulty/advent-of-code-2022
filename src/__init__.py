from pathlib import Path
from typing import Protocol, TypeVar


def load_data(data_file: Path) -> list[str]:
    with open(data_file) as data:
        return [*data]


T = TypeVar("T")


class Receiver(Protocol[T]):
    def receive(self, value: T) -> None:
        ...


def yes(_: T = None) -> bool:
    return True


def no(_: T = None) -> bool:
    return False
