import math
import unittest
from collections import deque
from dataclasses import asdict
from pathlib import Path

from src import load_data
from src.day11 import Item, KeepAway, Monkey, parse, parse_as_malformed_yaml


class Day11Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day11/example.txt"
        )
        cls.input_data: list[str] = load_data(
            Path(__file__).parent / "../src/day11/input.txt"
        )

    def test_example_parse_as_malformed_yaml(self):
        monkey_data = parse_as_malformed_yaml(self.example_data)
        self.assertEqual(4, len(monkey_data))
        self.assertEqual(
            {
                "Starting items": "79, 98",
                "Operation": "new = old * 19",
                "Test": "divisible by 23",
                "If true": "throw to monkey 2",
                "If false": "throw to monkey 3",
            },
            monkey_data["Monkey 0"],
        )

    def test_parse(self):
        monkeys = [*parse(self.example_data)]
        self.assertEqual(4, len(monkeys))
        self.assertEqual(
            Monkey(
                number=3,
                operation=Item.Add(3),
                test=Item.DivisibleBy(17),
                if_true=0,
                if_false=1,
                items=[Item(74)],
            ),
            monkeys[3],
        )

    def test_example_play_rounds_of_keep_away(self):
        game = KeepAway(players={m.number: m for m in parse(self.example_data)})

        game.play(num_rounds=10)
        self.assertEqual(
            [
                {0: [20, 23, 27, 26], 1: [2080, 25, 167, 207, 401, 1046], 2: [], 3: []},
                {0: [695, 10, 71, 135, 350], 1: [43, 49, 58, 55, 362], 2: [], 3: []},
                {0: [16, 18, 21, 20, 122], 1: [1468, 22, 150, 286, 739], 2: [], 3: []},
                {0: [491, 9, 52, 97, 248, 34], 1: [39, 45, 43, 258], 2: [], 3: []},
                {0: [15, 17, 16, 88, 1037], 1: [20, 110, 205, 524, 72], 2: [], 3: []},
                {0: [8, 70, 176, 26, 34], 1: [481, 32, 36, 186, 2190], 2: [], 3: []},
                {0: [162, 12, 14, 64, 732, 17], 1: [148, 372, 55, 72], 2: [], 3: []},
                {0: [51, 126, 20, 26, 136], 1: [343, 26, 30, 1546, 36], 2: [], 3: []},
                {0: [116, 10, 12, 517, 14], 1: [108, 267, 43, 55, 288], 2: [], 3: []},
                {0: [91, 16, 20, 98], 1: [481, 245, 22, 26, 1092, 30], 2: [], 3: []},
            ],
            list(map(lambda it: it.worry_levels, game.round_results)),
        )
        game.play(num_rounds=10)
        self.assertEqual(10605, game.round_results[-1].monkey_business_level)

    def test_solution_1(self):
        game = KeepAway(players={m.number: m for m in parse(self.input_data)})
        game.play(num_rounds=20)
        self.assertEqual(50172, game.round_results[-1].monkey_business_level)

    def test_example_long_game(self):
        monkeys = [*parse(self.example_data)]
        base = int(math.prod(m.test.factor for m in monkeys))
        game = KeepAway(
            players={m.number: m for m in monkeys},
            operation=Item.Mod(base),
            round_results=deque(maxlen=1),
        )

        game.play(num_rounds=1)
        self.assertEqual([2, 4, 3, 6], [m.inspection_count for m in monkeys])

        game.play(num_rounds=19)
        self.assertEqual([99, 97, 8, 103], [m.inspection_count for m in monkeys])

        game.play(num_rounds=980)
        self.assertEqual([5204, 4792, 199, 5192], [m.inspection_count for m in monkeys])

        game.play(num_rounds=1000)
        self.assertEqual(
            [10419, 9577, 392, 10391], [m.inspection_count for m in monkeys]
        )

        game.play(num_rounds=1000)
        self.assertEqual(
            [15638, 14358, 587, 15593], [m.inspection_count for m in monkeys]
        )

        game.play(num_rounds=7000)
        self.assertEqual(
            [52166, 47830, 1938, 52013], [m.inspection_count for m in monkeys]
        )
        self.assertEqual(2713310158, game.round_results[-1].monkey_business_level)

    def test_solution_2(self):
        monkeys = [*parse(self.input_data)]
        base = int(math.prod(m.test.factor for m in monkeys))
        game = KeepAway(
            players={m.number: m for m in monkeys},
            operation=Item.Mod(base),
            round_results=deque(maxlen=1),
        )

        game.play(num_rounds=10000)
        self.assertEqual(
            [10659, 70776, 73630, 109098, 106461, 62841, 61442, 50365],
            [m.inspection_count for m in monkeys],
        )
        self.assertEqual(11614682178, game.round_results[-1].monkey_business_level)
