from dataclasses import InitVar, dataclass, field
from enum import Enum
from functools import cached_property
from itertools import zip_longest
from math import prod
from typing import Iterator, Optional


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


def takeuntil(predicate, iterable):
    found = False
    for x in iterable:
        if found:
            break
        if predicate(x):
            found = True

        yield x


@dataclass(frozen=True)
class Forest:
    trees: InitVar[list[list[Tree]]]
    rows: list[list[Tree]] = field(init=False)

    def __post_init__(self, trees: list[list[Tree]]):
        object.__setattr__(
            self,
            "rows",
            [
                [
                    Tree(trees[i][j].height, location=(i, j))
                    for j in range(0, len(trees[i]))
                ]
                for i in range(0, len(trees))
            ],
        )

    def get_visible_trees(
        self, from_directions: set[Direction] = frozenset(iter(Direction))
    ) -> set[Tree]:
        visible_trees = set()

        if Direction.NORTH in from_directions:
            for column in self.columns:
                visible_trees |= get_visible_trees(c for c in column if c is not None)
        if Direction.SOUTH in from_directions:
            for column in zip_longest(*reversed(self.rows)):
                visible_trees |= get_visible_trees(c for c in column if c is not None)
        if Direction.EAST in from_directions:
            for row in self.rows:
                visible_trees |= get_visible_trees(iter(row))
        if Direction.WEST in from_directions:
            for row in self.rows:
                visible_trees |= get_visible_trees(reversed(row))

        return visible_trees

    @cached_property
    def columns(self):
        return [*zip_longest(*self.rows)]

    def get_scenic_score_by_location(self, location: tuple[int, int]):
        r, c = location
        trees_to_the_north = self.columns[c][r::-1][1:]
        trees_to_the_south = self.columns[c][r:][1:]
        trees_to_the_east = self.rows[r][c:][1:]
        trees_to_the_west = self.rows[r][c::-1][1:]
        return prod(
            map(
                lambda arr: len(
                    [*takeuntil(lambda t: t.height >= self.rows[r][c].height, arr)]
                ),
                [
                    trees_to_the_north,
                    trees_to_the_south,
                    trees_to_the_east,
                    trees_to_the_west,
                ],
            )
        )


def parse(data: list[str]):
    return Forest([[Tree(int(h)) for h in line.strip()] for line in data])
