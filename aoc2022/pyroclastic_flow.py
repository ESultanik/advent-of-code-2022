"""
--- Day 17: Pyroclastic Flow ---
Your handheld device has located an alternative exit from the cave for you and the elephants. The ground is rumbling almost continuously now, but the strange valves bought you some time. It's definitely getting warmer in here, though.

The tunnels eventually open into a very tall, narrow chamber. Large, oddly-shaped rocks are falling into the chamber from above, presumably due to all the rumbling. If you can't work out where the rocks will fall next, you might be crushed!

The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:

####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
The rocks fall in the order shown above: first the - shape, then the + shape, and so on. Once the end of the list is reached, the same order repeats: the - shape falls first, sixth, 11th, 16th, etc.

The rocks don't spin, but they do get pushed around by jets of hot gas coming out of the walls themselves. A quick scan reveals the effect the jets of hot gas will have on the rocks as they fall (your puzzle input).

For example, suppose this was the jet pattern in your cave:

>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
In jet patterns, < means a push to the left, while > means a push to the right. The pattern above means that the jets will push a falling rock right, then right, then right, then left, then left, then right, and so on. If the end of the list is reached, it repeats.

The tall, vertical chamber is exactly seven units wide. Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).

After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the direction indicated by the next symbol in the jet pattern) and then falling one unit down. If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock, the movement instead does not occur. If a downward movement would have caused a falling rock to move into the floor or an already-fallen rock, the falling rock stops where it is (having landed on something) and a new rock immediately begins falling.

Drawing falling rocks with @ and stopped rocks with #, the jet pattern in the example above manifests as follows:

The first rock begins falling:
|..@@@@.|
|.......|
|.......|
|.......|
+-------+

Jet of gas pushes rock right:
|...@@@@|
|.......|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
+-------+

Jet of gas pushes rock left:
|..@@@@.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|..####.|
+-------+

A new rock begins falling:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|...@...|
|..@@@..|
|...@...|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|..####.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|...#...|
|..###..|
|...#...|
|..####.|
+-------+

A new rock begins falling:
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|...#...|
|..###..|
|...#...|
|..####.|
+-------+
The moment each of the next few rocks begins falling, you would see this:

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|..#....|
|..#....|
|####...|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|..#....|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|.....#.|
|.....#.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|....##.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|##..##.|
|######.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+
To prove to the elephants your simulation is accurate, they want to know how tall the tower will get after 2022 rocks have stopped (but before the 2023rd rock begins falling). In this example, the tower of rocks will be 3068 units tall.

How many units tall will the tower of rocks be after 2022 rocks have stopped falling?
"""

from enum import Enum
import sys
from typing import Dict, Optional, Sequence, Set, TextIO, Tuple

from . import challenge, Path


Point = Tuple[int, int]


class Shape(Enum):
    H_BAR = "####"
    PLUS = ".#.\n###\n.#."
    BACK_L = "..#\n..#\n###"
    V_BAR = "#\n#\n#\n#"
    BOX = "##\n##"

    def __init__(self, shape: str):
        points = [
            (r, c)
            for r, row in enumerate(reversed(shape.split("\n")))
            for c, col in enumerate(row)
            if col == "#"
        ]
        self.points: Sequence[Point] = tuple(points)
        self.height: int = max(row for row, _ in self.points) + 1
        self.width: int = max(col for _, col in self.points) + 1

    def __str__(self):
        rows = [["."] * self.width for _ in range(self.height)]
        for row, col in self.points:
            rows[row][col] = "#"
        return "\n".join(("".join(row) for row in reversed(rows)))


class Tower:
    def __init__(self):
        self.tower: Dict[int, Set[int]] = {}
        self._height: int = 0

    @property
    def height(self) -> int:
        return self._height

    def __getitem__(self, point: Point) -> bool:
        return point in self

    def __contains__(self, point: Point):
        row, col = point
        if row not in self.tower:
            return False
        return col in self.tower[row]

    def can_add(self, at: Point, shape: Shape) -> bool:
        at_row, at_col = at
        return not any(self[(at_row + row, at_col + col)] for row, col in shape.points)

    def add(self, at: Point, shape: Shape) -> bool:
        if not self.can_add(at=at, shape=shape):
            # one of the points is already occupied
            return False
        at_row, at_col = at
        for shape_row, shape_col in shape.points:
            row = shape_row + at_row
            col = shape_col + at_col
            if row not in self.tower:
                tower_row = {col}
                self.tower[row] = tower_row
                self._height = max(self._height, row + 1)
            else:
                self.tower[row].add(col)
        return True


class Push(Enum):
    LEFT = ("<", -1)
    RIGHT = (">", 1)

    def __init__(self, symbol: str, col_delta: int):
        self.symbol: str = symbol
        self.col_delta: int = col_delta


class Cave:
    def __init__(self, jet_pattern: Sequence[Push], width: int = 7):
        self.jet_pattern: Sequence[Push] = jet_pattern
        self.jet_state: int = 0
        self.width: int = width
        self.tower: Tower = Tower()

    def drop(self, shape: Shape, print_steps: bool = False):
        row = self.tower.height + 3
        col = 2
        assert self.tower.can_add(at=(row, col), shape=shape)
        while True:
            if print_steps:
                self.print(at=(row, col), shape=shape)
            # first simulate the jet
            jet = self.jet_pattern[self.jet_state]
            if print_steps:
                print(jet.symbol)
            jet_col = col + jet.col_delta
            self.jet_state = (self.jet_state + 1) % len(self.jet_pattern)
            if jet_col >= 0 and jet_col + shape.width <= self.width \
                    and self.tower.can_add(at=(row, jet_col), shape=shape):
                # the jet moved the shape
                col = jet_col
                if print_steps:
                    self.print(at=(row, col), shape=shape)
            if row == 0 or not self.tower.can_add(at=(row - 1, col), shape=shape):
                # the block came to rest
                break
            row -= 1
        result = self.tower.add(at=(row, col), shape=shape)
        assert result
        if print_steps:
            self.print()

    def print(self, at: Optional[Point] = None, shape: Optional[Shape] = None, stream: TextIO = sys.stdout):
        max_row = self.tower.height + 3
        if at is not None and shape is not None:
            max_row = max(max_row, at[0] + shape.height - 1)
        for row in range(max_row, -1, -1):
            stream.write("|")
            for col in range(self.width):
                if at is not None and shape is not None:
                    row_within_shape = row - at[0]
                    col_within_shape = col - at[1]
                    if 0 <= row_within_shape < shape.height and 0 <= col_within_shape < shape.width \
                            and (row_within_shape, col_within_shape) in shape.points:
                        stream.write("@")
                        continue
                if self.tower[(row, col)]:
                    stream.write("#")
                else:
                    stream.write(".")
            stream.write("|\n")
        stream.write("+")
        stream.write("-" * self.width)
        stream.write("+\n\n")


@challenge(day=17)
def tower_height(path: Path) -> int:
    with open(path, "r") as f:
        jet_pattern = [
            [Push.LEFT, Push.RIGHT][c == ">"]
            for c in f.read()
            if c in "<>"
        ]
    cave = Cave(jet_pattern)
    shapes = [Shape.H_BAR, Shape.PLUS, Shape.BACK_L, Shape.V_BAR, Shape.BOX]
    for shape in shapes:
        print(str(shape))
        print()
    for rock in range(2022):
        cave.drop(shapes[rock % len(shapes)])  # , print_steps=True)
    return cave.tower.height
