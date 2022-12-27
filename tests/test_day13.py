import unittest
from pathlib import Path

from src import load_data
from src.day13 import Packet, get_decoder_key, parse, parse_pairs


class Day13Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day13/example.txt"
        )
        cls.input_data: list[str] = load_data(
            Path(__file__).parent / "../src/day13/input.txt"
        )

    def test_parse_example(self):
        packet_pairs = [*parse_pairs(self.example_data)]
        self.assertEqual(8, len(packet_pairs))
        self.assertEqual(
            (Packet([1, 1, 3, 1, 1]), Packet([1, 1, 5, 1, 1])), packet_pairs[0]
        )
        self.assertEqual(
            (
                Packet([1, [2, [3, [4, [5, 6, 7]]]], 8, 9]),
                Packet([1, [2, [3, [4, [5, 6, 0]]]], 8, 9]),
            ),
            packet_pairs[-1],
        )

    def test_example_compare_left_and_right(self):
        packet_pairs = parse_pairs(self.example_data)
        self.assertEqual(
            [
                True,
                True,
                False,
                True,
                False,
                True,
                False,
                False,
            ],
            [*map(lambda x: x[0] < x[1], packet_pairs)],
        )

    def test_example_decoder_key(self):
        packets = parse(self.example_data)
        self.assertEqual(
            140,
            get_decoder_key(packets, divider_packets=(Packet([[2]]), Packet([[6]]))),
        )

    def test_solution_1(self):
        packet_pairs = parse_pairs(self.input_data)
        self.assertEqual(
            5555,
            sum(
                map(
                    lambda x: x[0] + 1 if x[1][0] < x[1][1] else 0,
                    enumerate(packet_pairs),
                )
            ),
        )

    def test_solution_2(self):
        packets = parse(self.input_data)
        self.assertEqual(
            22852,
            get_decoder_key(packets, divider_packets=(Packet([[2]]), Packet([[6]]))),
        )
