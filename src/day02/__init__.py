from enum import Enum


class Play(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


PLAY_MAP = {
    "A X": (Play.ROCK, Play.ROCK),
    "A Y": (Play.ROCK, Play.PAPER),
    "A Z": (Play.ROCK, Play.SCISSORS),
    "B X": (Play.PAPER, Play.ROCK),
    "B Y": (Play.PAPER, Play.PAPER),
    "B Z": (Play.PAPER, Play.SCISSORS),
    "C X": (Play.SCISSORS, Play.ROCK),
    "C Y": (Play.SCISSORS, Play.PAPER),
    "C Z": (Play.SCISSORS, Play.SCISSORS),
}

OUTCOME_MAP = {
    "A X": (Play.ROCK, Play.SCISSORS),
    "A Y": (Play.ROCK, Play.ROCK),
    "A Z": (Play.ROCK, Play.PAPER),
    "B X": (Play.PAPER, Play.ROCK),
    "B Y": (Play.PAPER, Play.PAPER),
    "B Z": (Play.PAPER, Play.SCISSORS),
    "C X": (Play.SCISSORS, Play.PAPER),
    "C Y": (Play.SCISSORS, Play.SCISSORS),
    "C Z": (Play.SCISSORS, Play.ROCK),
}


def _play_score(play: Play) -> int:
    match play:
        case Play.ROCK:
            return 1
        case Play.PAPER:
            return 2
        case Play.SCISSORS:
            return 3


class Player(Enum):
    PLAYER_ONE = "player one"
    PLAYER_TWO = "player two"


def _outcome_score(player: Player, winner: Player | None):
    if winner == player:
        return 6
    elif winner == None:
        return 3
    else:
        return 0


class Round:
    def __init__(self, player_one_play: Play, player_two_play: Play):
        self.player_one_play = player_one_play
        self.player_two_play = player_two_play

    def __eq__(self, other):
        return (
            self.player_one_play == other.player_one_play
            and self.player_two_play == other.player_two_play
        )

    @staticmethod
    def by_play_mapping(round_data: str):
        return Round(*PLAY_MAP[round_data])

    @staticmethod
    def by_outcome_mapping(round_data: str):
        return Round(*OUTCOME_MAP[round_data])

    @property
    def winner(self) -> Player | None:
        if (
            self.player_one_play == Play.ROCK
            and self.player_two_play == Play.SCISSORS
            or self.player_one_play == Play.PAPER
            and self.player_two_play == Play.ROCK
            or self.player_one_play == Play.SCISSORS
            and self.player_two_play == Play.PAPER
        ):
            return Player.PLAYER_ONE
        elif (
            self.player_one_play == Play.ROCK
            and self.player_two_play == Play.PAPER
            or self.player_one_play == Play.PAPER
            and self.player_two_play == Play.SCISSORS
            or self.player_one_play == Play.SCISSORS
            and self.player_two_play == Play.ROCK
        ):
            return Player.PLAYER_TWO
        else:
            return None

    @property
    def player_two_score(self) -> int:
        return _play_score(self.player_two_play) + _outcome_score(
            Player.PLAYER_TWO, self.winner
        )

    @property
    def player_one_score(self) -> int:
        return _play_score(self.player_one_play) + _outcome_score(
            Player.PLAYER_ONE, self.winner
        )


class Tournament:
    def __init__(self, rounds: list[Round]):
        self.rounds = rounds

    def __eq__(self, other):
        return self.rounds == other.rounds

    @property
    def player_one_score(self) -> int:
        return sum([r.player_one_score for r in self.rounds])

    @property
    def player_two_score(self) -> int:
        return sum([r.player_two_score for r in self.rounds])


def load(data_file: str, round_parser=Round.by_play_mapping):
    rounds = []
    with open(data_file) as tournament_data:
        for line in tournament_data:
            rounds.append(round_parser(line.strip()))

    return Tournament(rounds=rounds)
