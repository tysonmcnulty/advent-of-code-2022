import unittest
from itertools import chain
from pathlib import Path
from typing import Optional

from src import load_data
from src.day14 import (
    Canvas,
    Cave,
    Extent,
    HorizontalSegment,
    Rock,
    Sand,
    Segment,
    Structure,
    parse,
    total_extent,
    with_floor,
)


class Day14Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day14/example.txt"
        )
        cls.input_data: list[str] = load_data(
            Path(__file__).parent / "../src/day14/input.txt"
        )

    @staticmethod
    def print(
        cave: Cave,
        current_unit: Optional[Sand.Unit] = None,
        frame: Optional[Extent] = None,
    ) -> list[str]:
        canvas = Canvas(extent=cave.extent)
        cave.render(canvas)
        if current_unit:
            current_unit.render(canvas)

        return canvas.print(frame=frame)

    def test_example_print(self):
        cave = Cave(structures=parse(self.example_data))
        self.assertEqual(
            [
                "......+...",
                "..........",
                "..........",
                "..........",
                "....#...##",
                "....#...#.",
                "..###...#.",
                "........#.",
                "........#.",
                "#########.",
            ],
            self.print(cave),
        )

    def test_example_print_with_frame(self):
        cave = Cave(structures=parse(self.example_data))
        self.assertEqual(
            [
                "..#..",
                "..#..",
                "###..",
            ],
            self.print(cave, frame=((496, 4), (500, 6))),
        )

    def test_example_simulate(self):
        cave = Cave(structures=parse(self.example_data))
        states = cave.simulate(should_stop=current_unit_not_in_cave_extent)
        current_state = next(states)

        self.assertEqual([Sand.Unit((500, 8))], list(cave.sand_units.values()))
        self.assertEqual(
            [
                (500, 8),
                (500, 7),
                (500, 6),
                (500, 5),
                (500, 4),
                (500, 3),
                (500, 2),
                (500, 1),
                (500, 0),
            ],
            current_state.paths[(500, 8)],
        )

        next(states)
        self.assertEqual(Sand.Unit((499, 8)), list(cave.sand_units.values())[-1])

        for _ in range(3):
            next(states)

        self.assertEqual(Sand.Unit((498, 8)), list(cave.sand_units.values())[-1])

        for _ in range(17):
            next(states)

        self.assertEqual(Sand.Unit((500, 2)), list(cave.sand_units.values())[-1])

        for _ in states:
            continue

        self.assertEqual(Sand.Unit((495, 8)), list(cave.sand_units.values())[-1])
        self.assertEqual(
            [
                "......+...",
                "..........",
                "......o...",
                ".....ooo..",
                "....#ooo##",
                "...o#ooo#.",
                "..###ooo#.",
                "....oooo#.",
                ".o.ooooo#.",
                "#########.",
            ],
            self.print(cave),
        )

    def test_example_simulate_with_floor(self):
        structures = parse(self.example_data)
        cave = Cave(with_floor(structures))
        states = cave.simulate()

        for _ in states:
            continue

        self.print(cave)
        self.assertEqual(93, len(cave.sand_units))
        self.assertEqual(
            [
                "............o............",
                "...........ooo...........",
                "..........ooooo..........",
                ".........ooooooo.........",
                "........oo#ooo##o........",
                ".......ooo#ooo#ooo.......",
                "......oo###ooo#oooo......",
                ".....oooo.oooo#ooooo.....",
                "....oooooooooo#oooooo....",
                "...ooo#########ooooooo...",
                "..ooooo.......ooooooooo..",
                "#########################",
            ],
            self.print(cave),
        )

    def test_solution_1(self):
        cave = Cave(structures=parse(self.input_data))
        states = cave.simulate(should_stop=current_unit_not_in_cave_extent)

        for _ in states:
            continue

        self.assertEqual(885, len(cave.sand_units))

    def test_solution_2(self):
        cave = Cave(structures=with_floor(parse(self.input_data)))
        states = cave.simulate()

        for _ in states:
            continue

        self.assertEqual(28691, len(cave.sand_units))


def current_unit_not_in_cave_extent(cave: Cave, current_unit: Sand.Unit) -> bool:
    return (
        current_unit is not None
        and not cave.extent[0] <= current_unit.location <= cave.extent[1]
    )
