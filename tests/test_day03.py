import unittest

from src.day03 import Compartment, Item, Rucksack, get_badges, get_unsorted_item, load


class Day03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load("tests/resources/day03/example.txt")
        cls.input = load("src/day03/input.txt")

    def test_compartment_from_str(self):
        self.assertEqual(
            Compartment(items=[Item("a"), Item("b"), Item("c")]),
            Compartment.from_str("abc"),
        )

    def test_load_example(self):
        self.assertEqual(
            self.example,
            [
                Rucksack(
                    (
                        Compartment.from_str("vJrwpWtwJgWr"),
                        Compartment.from_str("hcsFMMfFFhFp"),
                    )
                ),
                Rucksack(
                    (
                        Compartment.from_str("jqHRNqRjqzjGDLGL"),
                        Compartment.from_str("rsFMfFZSrLrFZsSL"),
                    )
                ),
                Rucksack(
                    (
                        Compartment.from_str("PmmdzqPrV"),
                        Compartment.from_str("vPwwTWBwg"),
                    )
                ),
                Rucksack(
                    (
                        Compartment.from_str("wMqvLMZHhHMvwLH"),
                        Compartment.from_str("jbvcjnnSBnvTQFn"),
                    )
                ),
                Rucksack(
                    (
                        Compartment.from_str("ttgJtRGJ"),
                        Compartment.from_str("QctTZtZT"),
                    )
                ),
                Rucksack(
                    (
                        Compartment.from_str("CrZsJsPPZsGz"),
                        Compartment.from_str("wwsLwLmpwMDw"),
                    )
                ),
            ],
        )

    def test_example_get_unsorted_item(self):
        self.assertEqual(
            [Item("p"), Item("L"), Item("P"), Item("v"), Item("t"), Item("s")],
            [get_unsorted_item(r) for r in self.example],
        )

    def test_example_get_unsorted_item_priorities(self):
        self.assertEqual(
            157, sum([get_unsorted_item(r).priority for r in self.example])
        )

    def test_example_get_badges(self):
        self.assertEqual(70, sum([i.priority for i in get_badges(self.example)]))

    def test_example_badge_priorities(self):
        self.assertEqual([Item("r"), Item("Z")], get_badges(self.example))

    def test_solution(self):
        self.assertEqual(7826, sum([get_unsorted_item(r).priority for r in self.input]))
        self.assertEqual(2577, sum([i.priority for i in get_badges(self.input)]))
