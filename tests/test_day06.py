import unittest
from pathlib import Path

from src import load_data
from src.day06 import DatastreamBuffer, parse


class Day06Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = [
            parse(d)
            for d in load_data(Path(__file__).parent / "resources/day06/example.txt")
        ]
        cls.input = parse(
            load_data(Path(__file__).parent / "../src/day06/input.txt")[0]
        )

    def test_load_example(self):
        self.assertEqual(
            self.examples,
            [
                DatastreamBuffer("mjqjpqmgbljsphdztnvjfqwrcgsmlb"),
                DatastreamBuffer("bvwbjplbgvbhsrlpgdmjqwftvncz"),
                DatastreamBuffer("nppdvjthqldpwncqszvftbrmjlhg"),
                DatastreamBuffer("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"),
                DatastreamBuffer("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"),
            ],
        )

    def test_first_start_of_packet_marker(self):
        self.assertEqual(
            [ex.first_start_of_packet_marker for ex in self.examples], [7, 5, 6, 10, 11]
        )

    def test_first_start_of_message_marker(self):
        self.assertEqual(
            [ex.first_start_of_message_marker for ex in self.examples],
            [19, 23, 23, 29, 26],
        )

    def test_solution(self):
        self.assertEqual(1802, self.input.first_start_of_packet_marker)
        self.assertEqual(3551, self.input.first_start_of_message_marker)
