import pprint
import unittest
from pathlib import Path

from src import load_data
from src.day07 import Directory, File, find_directories, parse


class Day07Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = parse(
            load_data(Path(__file__).parent / "resources/day07/example.txt")
        )
        cls.input = parse(load_data(Path(__file__).parent / "../src/day07/input.txt"))

    def test_load_example(self):
        expected = Directory(
            "/",
            frozenset(
                [
                    Directory(
                        "a",
                        frozenset(
                            [Directory("e", frozenset(), frozenset([File("i", 584)]))]
                        ),
                        frozenset(
                            [
                                File("f", 29116),
                                File("g", 2557),
                                File("h.lst", 62596),
                            ]
                        ),
                    ),
                    Directory(
                        "d",
                        frozenset(),
                        frozenset(
                            [
                                File("j", 4060174),
                                File("d.log", 8033020),
                                File("d.ext", 5626152),
                                File("k", 7214296),
                            ]
                        ),
                    ),
                ],
            ),
            frozenset([File("b.txt", 14848514), File("c.dat", 8504156)]),
        )
        self.assertEqual(expected, self.example)

    def test_find_directories(self):
        self.assertEqual(
            {"/", "a", "e", "d"}, {d.name for d in find_directories(self.example)}
        )
        self.assertEqual(
            95437,
            sum(
                d.size
                for d in find_directories(self.example, lambda d: d.size <= 100000)
            ),
        )

    def test_solutions(self):
        self.assertEqual(
            2061777,
            sum(
                d.size for d in find_directories(self.input, lambda d: d.size <= 100000)
            ),
        )
        total_disk_space = 70000000
        total_used_disk_space = self.input.size
        total_required_unused_disk_space = 30000000
        total_unused_disk_space = total_disk_space - total_used_disk_space
        total_required_disk_space = (
            total_required_unused_disk_space - total_unused_disk_space
        )

        def is_big_enough(d: Directory) -> bool:
            return d.size >= total_required_disk_space

        self.assertEqual(
            4473403,
            min(d.size for d in find_directories(self.input, is_big_enough)),
        )
