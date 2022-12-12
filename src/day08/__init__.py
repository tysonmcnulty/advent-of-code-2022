from dataclasses import dataclass, field, InitVar
from enum import Enum
from functools import cache
from itertools import zip_longest
from typing import Optional, Iterator


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


@dataclass(frozen=True)
class Tree:
    height: int
    location: Optional[tuple[int, int]] = None


def get_visible_trees(trees: Iterator[Tree]) -> set[Tree]:
    tallest_tree_so_far = next(trees)
    visible_trees = {tallest_tree_so_far}

    for tree in trees:
        if tree.height > tallest_tree_so_far.height:
            visible_trees.add(tree)
            tallest_tree_so_far = tree

    return visible_trees


@dataclass(frozen=True)
class Forest:
    from_trees: InitVar[list[list[Tree]]]
    trees: list[list[Tree]] = field(init=False)

    def __post_init__(self, from_trees: list[list[Tree]]):
        object.__setattr__(
            self,
            "trees",
            [
                [
                    Tree(from_trees[i][j].height, location=(i, j))
                    for j in range(0, len(from_trees[i]))
                ]
                for i in range(0, len(from_trees))
            ],
        )

    def get_visible_trees(
        self, from_directions: set[Direction] = frozenset(iter(Direction))
    ) -> set[Tree]:
        visible_trees = set()

        if Direction.NORTH in from_directions:
            for column in zip_longest(*self.trees):
                visible_trees |= get_visible_trees(c for c in column if c is not None)
        if Direction.SOUTH in from_directions:
            for column in zip_longest(*reversed(self.trees)):
                visible_trees |= get_visible_trees(c for c in column if c is not None)
        if Direction.EAST in from_directions:
            for row in self.trees:
                visible_trees |= get_visible_trees(iter(row))
        if Direction.WEST in from_directions:
            for row in self.trees:
                visible_trees |= get_visible_trees(reversed(row))

        return visible_trees


def parse(data: list[str]):
    return Forest([[Tree(int(h)) for h in line.strip()] for line in data])
