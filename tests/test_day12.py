import unittest
from pathlib import Path

from src import load_data
from src.day12 import Heightmap, Hiker, Square, parse


class Day12Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day12/example.txt"
        )
        cls.input_data: list[str] = load_data(
            Path(__file__).parent / "../src/day12/input.txt"
        )

    def test_parse_example(self):
        hiker = Hiker(
            heightmap=Heightmap(
                [
                    "Sabqponm",
                    "abcryxxl",
                    "accszExk",
                    "acctuvwj",
                    "abdefghi",
                ]
            ),
            search_mode=Hiker.SearchMode.FORWARD,
        )
        self.assertEqual(
            hiker,
            parse(self.example_data),
        )
        heightmap = hiker.heightmap
        self.assertEqual(heightmap.square_at((2, 5)), heightmap.best_signal_location)
        self.assertEqual(heightmap.square_at((0, 0)), heightmap.current_location)
        self.assertEqual(heightmap.square_at((0, 0)), hiker.location)

    def test_example_navigate(self):
        hiker = parse(self.example_data)
        paths = hiker.navigate()
        best_path = paths[hiker.heightmap.best_signal_location.position]
        self.assertEqual(31, len(best_path) - 1)

    def test_example_navigate_in_reverse(self):
        hiker = parse(self.example_data)
        hiker.location = hiker.heightmap.best_signal_location
        hiker.search_mode = Hiker.SearchMode.REVERSE
        first_explored_low_square: Square | None = None

        def on_first_explored_low_square(square: Square) -> bool:
            nonlocal first_explored_low_square
            if square.elevation == "a":
                first_explored_low_square = square
                return True

            return False

        paths = hiker.navigate(should_stop=on_first_explored_low_square)
        self.assertNotEqual(None, first_explored_low_square)
        best_path = paths[first_explored_low_square.position]
        self.assertEqual(29, len(best_path) - 1)

    def test_solution_1(self):
        hiker = parse(self.input_data)
        paths = hiker.navigate()
        best_path = paths[hiker.heightmap.best_signal_location.position]
        self.assertEqual(437, len(best_path) - 1)

    def test_solution_2(self):
        hiker = parse(self.input_data)
        hiker.location = hiker.heightmap.best_signal_location
        hiker.search_mode = Hiker.SearchMode.REVERSE
        first_explored_low_square: Square | None = None

        def on_first_explored_low_square(square: Square) -> bool:
            nonlocal first_explored_low_square
            if square.elevation == "a":
                first_explored_low_square = square
                return True

            return False

        paths = hiker.navigate(should_stop=on_first_explored_low_square)
        self.assertNotEqual(None, first_explored_low_square)
        best_path = paths[first_explored_low_square.position]
        self.assertEqual(430, len(best_path) - 1)
