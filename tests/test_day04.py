import unittest
from pathlib import Path

from src.day04 import Assignment, load


class Day04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day04/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day04/input.txt")

    def test_from_str(self):
        self.assertEqual(Assignment(1, 10), Assignment.from_str("1-10"))

    def test_section_ids(self):
        self.assertEqual([5, 6, 7, 8], list(Assignment(5, 8).section_ids))

    def test_load_example(self):
        self.assertEqual(
            self.example,
            [
                (Assignment(2, 4), Assignment(6, 8)),
                (Assignment(2, 3), Assignment(4, 5)),
                (Assignment(5, 7), Assignment(7, 9)),
                (Assignment(2, 8), Assignment(3, 7)),
                (Assignment(6, 6), Assignment(4, 6)),
                (Assignment(2, 6), Assignment(4, 8)),
            ],
        )

    def test_example_overlap(self):
        self.assertEqual(
            [
                None,
                None,
                Assignment(7, 7),
                Assignment(3, 7),
                Assignment(6, 6),
                Assignment(4, 6),
            ],
            [a.overlap(b) for (a, b) in self.example],
        )

    def test_solution(self):
        self.assertEqual(503, sum(a.overlap(b) in set((a, b)) for (a, b) in self.input))
        self.assertEqual(827, sum(bool(a.overlap(b)) for (a, b) in self.input))
