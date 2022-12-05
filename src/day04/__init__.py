from typing import Iterator, Self


def load(data_file: str):
    assignment_pairs = []
    with open(data_file) as data:
        for line in data:
            pair_data = line.strip().split(",")
            assignment_pairs.append(tuple(Assignment.from_str(d) for d in pair_data))

    return assignment_pairs


SectionID = int


class Assignment:
    def __init__(self, low: SectionID, high: SectionID):
        self.low = low
        self.high = high

    def __eq__(self, other):
        if isinstance(other, Assignment):
            return self.low == other.low and self.high == other.high
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.low, self.high))

    @property
    def section_ids(self) -> Iterator[SectionID]:
        return range(self.low, self.high + 1)

    def overlap(self, other: Self) -> Self:
        max_low = max(self.low, other.low)
        min_high = min(self.high, other.high)
        return Assignment(max_low, min_high) if max_low <= min_high else None

    @staticmethod
    def from_str(data: str):
        return Assignment(*[int(id) for id in data.split("-")])
