import unittest
from pathlib import Path

from src import load_data
from src.day08 import Forest, Tree, parse, Direction


class Day08Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example: Forest = parse(
            load_data(Path(__file__).parent / "resources/day08/example.txt")
        )
        cls.input: Forest = parse(
            load_data(Path(__file__).parent / "../src/day08/input.txt")
        )

    def test_load_example(self):
        self.assertEqual(
            Forest(
                [
                    [Tree(3), Tree(0), Tree(3), Tree(7), Tree(3)],
                    [Tree(2), Tree(5), Tree(5), Tree(1), Tree(2)],
                    [Tree(6), Tree(5), Tree(3), Tree(3), Tree(2)],
                    [Tree(3), Tree(3), Tree(5), Tree(4), Tree(9)],
                    [Tree(3), Tree(5), Tree(3), Tree(9), Tree(0)],
                ]
            ),
            self.example,
        )

    def test_get_tree_in_forest(self):
        self.assertEqual(Tree(3, location=(0, 0)), self.example.trees[0][0])

    def test_get_visible_trees_from_north_and_south(self):
        forest = Forest(
            [
                [Tree(3)],
                [Tree(2)],
                [Tree(6)],
                [Tree(3)],
                [Tree(3)],
            ]
        )
        self.assertEqual(
            {Tree(3, location=(0, 0)), Tree(6, location=(2, 0)), Tree(3, location=(4, 0))},
            forest.get_visible_trees(from_directions={Direction.NORTH, Direction.SOUTH}),
        )

    def test_get_visible_trees_from_east_and_west(self):
        forest = Forest(
            [
                [Tree(3), Tree(0), Tree(3), Tree(7), Tree(3)],
            ]
        )
        self.assertEqual(
            {Tree(3, location=(0, 0)), Tree(7, location=(0, 3)), Tree(3, location=(0, 4))},
            forest.get_visible_trees(from_directions={Direction.EAST, Direction.WEST}),
        )

    def test_example_get_visible_trees(self):
        self.assertEqual(21, len(self.example.get_visible_trees()))

    def test_solutions(self):
        self.assertEqual(1546, len(self.input.get_visible_trees()))


