import unittest

from src.day01 import load_cals, top_3_cals


class DayO1Tests(unittest.TestCase):
    def test_load_cals(self):
        self.assertEqual(
            24000,
            load_cals("data/day01_calories_test.txt"),
        )
        # Part 1
        self.assertEqual(70374, load_cals("data/day01_calories_bm.txt"))
        # self.assertEqual(2000, len(load_cals("data/day01_calories_tm.txt")))

    # Part 2
    def test_top_3_cals(self):
        self.assertEqual(45000, top_3_cals("data/day01_calories_test.txt"))
        self.assertEqual(204610, top_3_cals("data/day01_calories_bm.txt"))
