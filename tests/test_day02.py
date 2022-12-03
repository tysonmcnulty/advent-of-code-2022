import unittest

from src.day02 import load, Tournament, Round, Play, Player


class Day02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load("tests/resources/day02/example.txt")
        cls.input = load("src/day02/input.txt")

    def test_round_from_str(self):
        self.assertEqual(Round(Play.ROCK, Play.SCISSORS), Round.from_str("A Z"))

    def test_load_example(self):
        self.assertEqual(
            self.example,
            Tournament(
                rounds=[
                    Round.from_str("A Y"),
                    Round.from_str("B X"),
                    Round.from_str("C Z"),
                ]
            ),
        )

    def test_round_winner(self):
        self.assertEqual(Player.PLAYER_ONE, Round.from_str("A Z").winner)
        self.assertEqual(Player.PLAYER_ONE, Round.from_str("B X").winner)
        self.assertEqual(Player.PLAYER_ONE, Round.from_str("C Y").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.from_str("A Y").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.from_str("B Z").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.from_str("C X").winner)
        self.assertEqual(None, Round.from_str("A X").winner)
        self.assertEqual(None, Round.from_str("B Y").winner)
        self.assertEqual(None, Round.from_str("C Z").winner)

    def test_round_score_example(self):
        self.assertEqual([8, 1, 6], [r.player_two_score for r in self.example.rounds])
        self.assertEqual([1, 8, 6], [r.player_one_score for r in self.example.rounds])

    def test_tournament_score_example(self):
        self.assertEqual(15, self.example.player_one_score)
        self.assertEqual(15, self.example.player_two_score)

    def test_solutions(self):
        self.assertEqual(14264, self.input.player_two_score)
