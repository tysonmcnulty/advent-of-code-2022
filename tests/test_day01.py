import unittest
from pathlib import Path

from src.day01 import (
    Elf,
    FoodItem,
    get_max_elf_calorie_count,
    get_top_three_elf_calorie_counts,
    load,
)


class Day01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day01/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day01/input.txt")

    def test_load_example(self):
        self.assertEqual(
            self.example,
            [
                Elf(
                    food_items=[
                        FoodItem(calorie_count=1000),
                        FoodItem(calorie_count=2000),
                        FoodItem(calorie_count=3000),
                    ]
                ),
                Elf(
                    food_items=[
                        FoodItem(calorie_count=4000),
                    ]
                ),
                Elf(
                    food_items=[
                        FoodItem(calorie_count=5000),
                        FoodItem(calorie_count=6000),
                    ]
                ),
                Elf(
                    food_items=[
                        FoodItem(calorie_count=7000),
                        FoodItem(calorie_count=8000),
                        FoodItem(calorie_count=9000),
                    ]
                ),
                Elf(
                    food_items=[
                        FoodItem(calorie_count=10000),
                    ]
                ),
            ],
        )

    def test_get_max_calorie_count(self):
        self.assertEqual(get_max_elf_calorie_count(self.example), 24000)

    def test_get_top_three_elf_calorie_counts(self):
        self.assertEqual(
            get_top_three_elf_calorie_counts(self.example), [24000, 11000, 10000]
        )

    def test_solutions(self):
        self.assertEqual(get_max_elf_calorie_count(self.input), 68292)
        self.assertEqual(sum(get_top_three_elf_calorie_counts(self.input)), 203203)
