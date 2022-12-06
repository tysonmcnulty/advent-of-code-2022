import unittest

from src.day05 import Crate, Ship, Stack, Step, Strategy, load_data, parse


class Day05Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data = load_data("tests/resources/day05/example.txt")
        cls.input_data = load_data("src/day05/input.txt")

    def test_load_example(self):
        self.assertEqual(
            parse(self.example_data),
            (
                Ship(
                    [
                        Stack("1", [Crate("Z"), Crate("N")]),
                        Stack("2", [Crate("M"), Crate("C"), Crate("D")]),
                        Stack("3", [Crate("P")]),
                    ]
                ),
                [
                    Step(1, "2", "1"),
                    Step(3, "1", "3"),
                    Step(2, "2", "1"),
                    Step(1, "1", "2"),
                ],
            ),
        )

    def test_example_run_crane(self):
        (ship, steps) = parse(self.example_data)
        ship.run_crane(steps)
        self.assertEqual(
            ship,
            Ship(
                [
                    Stack("1", [Crate("C")]),
                    Stack("2", [Crate("M")]),
                    Stack("3", [Crate("P"), Crate("D"), Crate("N"), Crate("Z")]),
                ]
            ),
        )

    def test_example_run_crate_mover_9001(self):
        (ship, steps) = parse(self.example_data)
        ship.run_crane(steps, strategy=Strategy.CRATE_MOVER_9001)
        self.assertEqual(
            ship,
            Ship(
                [
                    Stack("1", [Crate("M")]),
                    Stack("2", [Crate("C")]),
                    Stack("3", [Crate("P"), Crate("Z"), Crate("N"), Crate("D")]),
                ]
            ),
        )

    def test_solution(self):
        (ship, steps) = parse(self.input_data)
        ship.run_crane(steps)
        self.assertEqual(
            "QMBMJDFTD", "".join(stack.crates[-1].label for stack in ship.stacks)
        )

        (ship, steps) = parse(self.input_data)
        ship.run_crane(steps, strategy=Strategy.CRATE_MOVER_9001)
        self.assertEqual(
            "NBTVTJNFJ", "".join(stack.crates[-1].label for stack in ship.stacks)
        )
