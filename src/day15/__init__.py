import re
from collections.abc import Container
from dataclasses import InitVar, dataclass, field
from typing import Any, Iterable, Iterator, Optional, Self, overload

Location = tuple[int, int]


@dataclass(frozen=True)
class Beacon:
    location: Location


@dataclass(frozen=True)
class Row:
    y: int


@dataclass(frozen=True)
class Interval:
    start: Location
    end: Location

    def __or__(self, other) -> Optional[Self]:
        if not isinstance(other, Interval):
            return NotImplemented

        min_start, max_start = tuple(sorted((self.start, other.start)))
        min_end, max_end = tuple(sorted((self.end, other.end)))
        return None if min_end[0] + 1 < max_start[0] else Interval(min_start, max_end)

    def __len__(self):
        return self.end[0] - self.start[0] + 1

    @staticmethod
    def merge(intervals: Iterable[Self]) -> Iterable[Self]:
        sorted_intervals = sorted(intervals, key=lambda i: i.start)
        if len(sorted_intervals) < 1:
            return []

        current_interval = sorted_intervals[0]
        for interval in sorted_intervals[1:]:
            if merged_interval := interval | current_interval:
                current_interval = merged_interval
            else:
                yield current_interval
                current_interval = interval

        yield current_interval


@overload
def distance(a: Row, b: Location) -> int:
    ...


@overload
def distance(a: Location, b: Row) -> int:
    ...


@overload
def distance(a: Location, b: Location) -> int:
    ...


def distance(a, b) -> int:
    _a: Location = (b[0], a.y) if isinstance(a, Row) else a
    _b: Location = (a[0], b.y) if isinstance(b, Row) else b

    return abs(_b[0] - _a[0]) + abs(_b[1] - _a[1])


@dataclass(frozen=True)
class Scanner:
    location: Location
    range_radius: InitVar[int]
    range: "Scanner.Range" = field(init=False)

    def __post_init__(self, range_radius: int):
        object.__setattr__(
            self, "range", Scanner.Range(center=self.location, radius=range_radius)
        )

    @dataclass(frozen=True)
    class Range(Container[Location]):
        center: Location
        radius: int

        def __contains__(self, obj: Any) -> bool:
            return distance(obj, self.center) <= self.radius

    def scan(self, row: Row) -> Optional[Interval]:
        h = distance(row, self.location)
        r = self.range.radius
        x = self.location[0]
        if h > r:
            return None

        return Interval(start=(x - (r - h), row.y), end=(x + (r - h), row.y))


def parse(data: list[str]) -> tuple[set[Scanner], set[Beacon]]:
    scanners: set[Scanner] = set()
    beacons: set[Beacon] = set()

    for line in data:
        scanner_x, scanner_y, beacon_x, beacon_y = re.match(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        ).group(1, 2, 3, 4)
        scanner_location: Location = (int(scanner_x), int(scanner_y))
        beacon_location: Location = (int(beacon_x), int(beacon_y))
        scanners.add(
            Scanner(
                location=scanner_location,
                range_radius=distance(scanner_location, beacon_location),
            )
        )
        beacons.add(Beacon(location=beacon_location))

    return scanners, beacons
