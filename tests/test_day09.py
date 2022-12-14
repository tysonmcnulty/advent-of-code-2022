import unittest
from pathlib import Path

from src import load_data
from src.day09 import Direction, Move, Rope, Segment, link, parse, record_tail_positions


class Day09Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day09/example.txt"
        )
        cls.longer_example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day09/longer_example.txt"
        )
        cls.input_data: list[str] = load_data(
            Path(__file__).parent / "../src/day09/input.txt"
        )

    def test_load_example(self):
        self.assertEqual(
            [
                Move(Direction.RIGHT),
                Move(Direction.RIGHT),
                Move(Direction.RIGHT),
                Move(Direction.RIGHT),
                Move(Direction.UP),
                Move(Direction.UP),
                Move(Direction.UP),
                Move(Direction.UP),
                Move(Direction.LEFT),
                Move(Direction.LEFT),
                Move(Direction.LEFT),
                Move(Direction.DOWN),
                Move(Direction.RIGHT),
                Move(Direction.RIGHT),
                Move(Direction.RIGHT),
                Move(Direction.RIGHT),
                Move(Direction.DOWN),
                Move(Direction.LEFT),
                Move(Direction.LEFT),
                Move(Direction.LEFT),
                Move(Direction.LEFT),
                Move(Direction.LEFT),
                Move(Direction.RIGHT),
                Move(Direction.RIGHT),
            ],
            [*parse(self.example_data)],
        )

    def test_link(self):
        segments = [Segment((0, 0)), Segment((0, 0)), Segment((0, 0)), Segment((0, 0))]
        segments[0].linked_to = segments[1]
        segments[1].linked_to = segments[2]
        segments[2].linked_to = segments[3]
        self.assertEqual(
            segments,
            link([Segment((0, 0)), Segment((0, 0)), Segment((0, 0)), Segment((0, 0))]),
        )

    def test_rope_with_many_segments(self):
        segments = [Segment((0, 0)), Segment((0, 0)), Segment((0, 0)), Segment((0, 0))]
        link(segments)
        rope = Rope(num_segments=4)
        self.assertEqual(segments, [*rope.segments])

    def test_example_moves(self):
        rope = Rope()
        moves = parse(self.example_data)
        rope.move(next(moves))
        self.assertEqual(link([Segment((0, 1)), Segment((0, 0))]), [*rope.segments])
        rope.move(next(moves))
        self.assertEqual(link([Segment((0, 2)), Segment((0, 1))]), [*rope.segments])
        rope.move(next(moves))
        rope.move(next(moves))
        rope.move(next(moves))
        self.assertEqual(link([Segment((-1, 4)), Segment((0, 3))]), [*rope.segments])
        rope.move(next(moves))
        self.assertEqual(link([Segment((-2, 4)), Segment((-1, 4))]), [*rope.segments])

    def test_example_tail_positions(self):
        self.assertEqual(
            13, len(record_tail_positions(Rope(), parse(self.example_data)))
        )
        self.assertEqual(
            1,
            len(record_tail_positions(Rope(num_segments=10), parse(self.example_data))),
        )

    def test_longer_example_tail_positions(self):
        self.assertEqual(
            36,
            len(
                record_tail_positions(
                    Rope(num_segments=10), parse(self.longer_example_data)
                )
            ),
        )

    def test_solutions(self):
        self.assertEqual(
            6090, len(record_tail_positions(Rope(), parse(self.input_data)))
        )
        self.assertEqual(
            2566,
            len(record_tail_positions(Rope(num_segments=10), parse(self.input_data))),
        )
