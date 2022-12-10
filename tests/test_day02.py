import unittest
from pathlib import Path

from src.day02 import Play, Player, Round, Tournament, load


class Day02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day02/example.txt")
        cls.example_by_outcome_mapping = load(
            Path(__file__).parent / "resources/day02/example.txt",
            Round.by_outcome_mapping,
        )
        cls.input = load(Path(__file__).parent / "../src/day02/input.txt")
        cls.input_by_outcome_mapping = load(
            Path(__file__).parent / "../src/day02/input.txt", Round.by_outcome_mapping
        )

    def test_round_from_str(self):
        self.assertEqual(Round(Play.ROCK, Play.SCISSORS), Round.by_play_mapping("A Z"))

    def test_load_example(self):
        self.assertEqual(
            self.example,
            Tournament(
                rounds=[
                    Round.by_play_mapping("A Y"),
                    Round.by_play_mapping("B X"),
                    Round.by_play_mapping("C Z"),
                ]
            ),
        )

    def test_round_by_play_mapping_winner(self):
        self.assertEqual(Player.PLAYER_ONE, Round.by_play_mapping("A Z").winner)
        self.assertEqual(Player.PLAYER_ONE, Round.by_play_mapping("B X").winner)
        self.assertEqual(Player.PLAYER_ONE, Round.by_play_mapping("C Y").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.by_play_mapping("A Y").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.by_play_mapping("B Z").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.by_play_mapping("C X").winner)
        self.assertEqual(None, Round.by_play_mapping("A X").winner)
        self.assertEqual(None, Round.by_play_mapping("B Y").winner)
        self.assertEqual(None, Round.by_play_mapping("C Z").winner)

    def test_round_by_outcome_mapping_winner(self):
        self.assertEqual(Player.PLAYER_ONE, Round.by_outcome_mapping("A X").winner)
        self.assertEqual(Player.PLAYER_ONE, Round.by_outcome_mapping("B X").winner)
        self.assertEqual(Player.PLAYER_ONE, Round.by_outcome_mapping("C X").winner)
        self.assertEqual(None, Round.by_outcome_mapping("A Y").winner)
        self.assertEqual(None, Round.by_outcome_mapping("B Y").winner)
        self.assertEqual(None, Round.by_outcome_mapping("C Y").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.by_outcome_mapping("A Z").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.by_outcome_mapping("B Z").winner)
        self.assertEqual(Player.PLAYER_TWO, Round.by_outcome_mapping("C Z").winner)

    def test_round_score_example(self):
        self.assertEqual([8, 1, 6], [r.player_two_score for r in self.example.rounds])
        self.assertEqual([1, 8, 6], [r.player_one_score for r in self.example.rounds])

    def test_tournament_score_example(self):
        self.assertEqual(15, self.example.player_one_score)
        self.assertEqual(15, self.example.player_two_score)

    def test_round_score_example_by_outcome_mapping(self):
        self.assertEqual(
            [4, 1, 7],
            [r.player_two_score for r in self.example_by_outcome_mapping.rounds],
        )
        self.assertEqual(
            [4, 8, 3],
            [r.player_one_score for r in self.example_by_outcome_mapping.rounds],
        )

    def test_solutions(self):
        self.assertEqual(14264, self.input.player_two_score)
        self.assertEqual(12382, self.input_by_outcome_mapping.player_two_score)
