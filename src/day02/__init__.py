from enum import Enum


def load(data_file: str):
    rounds = []
    with open(data_file) as tournament_data:
        for line in tournament_data:
            rounds.append(Round.from_str(line.strip()))

    return Tournament(rounds=rounds)


class Play(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


PLAY_DATA_MAP = {
    "A": Play.ROCK,
    "B": Play.PAPER,
    "C": Play.SCISSORS,
    "X": Play.ROCK,
    "Y": Play.PAPER,
    "Z": Play.SCISSORS,
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
    def from_str(round_data: str):
        play_data = round_data.split(" ")
        print(play_data)
        return Round(
            PLAY_DATA_MAP[play_data[0]],
            PLAY_DATA_MAP[play_data[1]],
        )

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
