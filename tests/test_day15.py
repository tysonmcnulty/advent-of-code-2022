import unittest
from itertools import chain, pairwise
from pathlib import Path
from typing import Iterable

from src import load_data
from src.day15 import Beacon, Interval, Location, Row, Scanner, distance, parse


class Day15Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day15/example.txt"
        )
        cls.input_data: list[str] = load_data(
            Path(__file__).parent / "../src/day15/input.txt"
        )

    def test_distance(self):
        self.assertEqual(0, distance((0, 0), (0, 0)))
        self.assertEqual(2, distance((3, 2), (2, 3)))
        self.assertEqual(13, distance((10, 2), (3, 8)))

    def test_scanner(self):
        scanner = Scanner(location=(0, 0), range_radius=10)
        self.assertTrue((0, 0) in scanner.range)
        self.assertFalse((4, 7) in scanner.range)
        self.assertTrue((-2, -8) in scanner.range)

    def test_example_parse(self):
        scanners, beacons = parse(self.example_data)
        self.assertTrue(Scanner((2, 18), 7) in scanners)
        self.assertTrue(Beacon((-2, 15)) in beacons)
        self.assertTrue(Scanner((20, 1), 7) in scanners)
        self.assertTrue(Beacon((15, 3)) in beacons)

    def test_scan(self):
        scanner = Scanner(location=(0, 0), range_radius=10)
        self.assertEqual(Interval(start=(-5, 5), end=(5, 5)), scanner.scan(Row(y=5)))
        self.assertEqual(Interval(start=(-1, -9), end=(1, -9)), scanner.scan(Row(y=-9)))
        self.assertEqual(None, scanner.scan(Row(y=11)))

    def test_merge(self):
        intervals = [
            Interval((14, 0), (19, 0)),
            Interval((4, 0), (8, 0)),
            Interval((-3, 0), (3, 0)),
            Interval((8, 0), (12, 0)),
            Interval((16, 0), (17, 0)),
            Interval((-10, 0), (-3, 0)),
        ]
        self.assertEqual(
            [
                Interval((-10, 0), (12, 0)),
                Interval((14, 0), (19, 0)),
            ],
            [*Interval.merge(intervals)],
        )

    def test_example_scan_row(self):
        scanners, beacons = parse(self.example_data)
        row = Row(y=10)
        scans = (s.scan(row) for s in scanners)
        intervals = Interval.merge(filter(lambda it: it is not None, scans))
        self.assertEqual(
            26,
            sum(map(len, intervals))
            - sum(map(lambda it: it.location[1] == row.y, chain(scanners, beacons))),
        )

    def test_example_scan_cave(self):
        scanners, beacons = parse(self.example_data)
        gaps = [*find_gaps(scanners, extent=((0, 0), (20, 20)))]
        self.assertEqual(1, len(gaps))
        self.assertEqual(1, len(gaps[0]))
        self.assertEqual((14, 11), gaps[0].start)
        self.assertEqual((14, 11), gaps[0].end)

    def test_solution_1(self):
        scanners, beacons = parse(self.input_data)
        row = Row(y=2000000)
        scans = (s.scan(row) for s in scanners)
        intervals = Interval.merge(filter(lambda it: it is not None, scans))
        self.assertEqual(
            5564017,
            sum(map(len, intervals))
            - sum(map(lambda it: it.location[1] == row.y, chain(scanners, beacons))),
        )

    def test_solution_2(self):
        scanners, beacons = parse(self.input_data)
        gaps = [*find_gaps(scanners, extent=((2880000, 3390000), (2890000, 3400000)))]
        print(gaps)
        self.assertEqual(1, len(gaps))
        self.assertEqual(1, len(gaps[0]))
        self.assertEqual(11558423398893, gaps[0].start[0] * 4000000 + gaps[0].start[1])


def find_gaps(
    scanners: set[Scanner], extent: (Location, Location)
) -> Iterable[Location]:
    for y in range(extent[0][1], extent[1][1] + 1):
        row = Row(y)
        if y % 10000 == 0:
            print(row)

        scans = (s.scan(row) for s in scanners)
        intervals = Interval.merge(filter(lambda it: it is not None, scans))
        if pair_with_gap := next(
            filter(
                lambda pair: extent[0][0] <= pair[0].end[0] + 1 <= extent[1][0],
                pairwise(intervals),
            ),
            None,
        ):
            yield Interval(
                (pair_with_gap[0].end[0] + 1, y), (pair_with_gap[1].start[0] - 1, y)
            )
