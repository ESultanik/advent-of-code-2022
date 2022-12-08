from enum import Enum
from typing import Dict, Iterator, List, Optional, Set, Tuple

from . import challenge, Path

"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
"""


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

    @property
    def opposite(self) -> "Direction":
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.EAST:
            return Direction.WEST
        else:
            return Direction.EAST


class Tree:
    def __init__(self, row: int, col: int, height: int):
        self.row: int = row
        self.col: int = col
        self.height: int = height
        self._neighbors: Dict[Direction, Optional[Tree]] = {
            Direction.NORTH: None,
            Direction.SOUTH: None,
            Direction.EAST: None,
            Direction.WEST: None
        }
        self.max_height: Dict[Direction, Optional[int]] = {
            Direction.NORTH: None,
            Direction.SOUTH: None,
            Direction.EAST: None,
            Direction.WEST: None
        }
        self._visible: Dict[Direction, Optional[bool]] = {
            Direction.NORTH: None,
            Direction.SOUTH: None,
            Direction.EAST: None,
            Direction.WEST: None
        }

    @property
    def visible(self) -> Optional[bool]:
        if any(v for v in self._visible.values()):
            return True
        elif all(v is not None and not v for v in self._visible.values()):
            return False
        else:
            return None

    def is_visible_from(self, direction: Direction) -> Optional[bool]:
        return self._visible[direction]

    def set_max_height(self, max_height: int, in_direction: Direction):
        if max_height == self.max_height[in_direction]:
            return
        assert self.max_height[in_direction] is None
        self._visible[in_direction] = max_height < self.height
        # print(f"({self.row}, {self.col}).max_height in {in_direction} = {max_height};\t"
        #       f"visible = {self.is_visible_from(in_direction)}")
        max_height = max(max_height, self.height)
        self.max_height[in_direction] = max_height
        # propagate the visibility
        neighbor = self._neighbors[in_direction.opposite]
        if neighbor is not None:
            neighbor.set_max_height(max_height, in_direction)

    def add_neighbor(self, tree: "Tree", direction: Direction):
        if self._neighbors[direction] is not None:
            if self._neighbors[direction] is tree:
                return
            raise ValueError()
        self._neighbors[direction] = tree
        if self.max_height[direction] is None and tree.max_height[direction] is not None:
            self.set_max_height(tree.max_height[direction], direction)
        if tree.max_height[direction.opposite] is None and self.max_height[direction.opposite] is not None:
            tree.set_max_height(self.max_height[direction.opposite], direction.opposite)

    def __eq__(self, other):
        return isinstance(other, Tree) and other.row == self.row and other.col == self.col

    def __hash__(self):
        return hash((self.row, self.col))


HeightMatrix = List[List[int]]


def load(path: Path) -> HeightMatrix:
    rows: HeightMatrix = []
    with open(path, "r") as f:
        for line in f:
            rows.append([int(height) for height in line.strip()])
    assert all(len(r) == len(rows[0]) for r in rows[1:])
    return rows


def neighborhood(row: int, col: int, width: int, height: int) -> Iterator[Tuple[int, int, Direction]]:
    for rdelta, cdelta, direction in (
            (-1, 0, Direction.NORTH), (0, -1, Direction.WEST), (0, 1, Direction.EAST), (1, 0, Direction.SOUTH)
    ):
        r, c = row + rdelta, col + cdelta
        if 0 <= r < height and 0 <= c < width:
            yield r, c, direction


class Forest:
    def __init__(self, trees: List[List[Tree]]):
        self.trees: List[List[Tree]] = trees

    def __iter__(self) -> Iterator[Tree]:
        for row in self.trees:
            yield from row

    def __getitem__(self, row: int) -> List[Tree]:
        return self.trees[row]

    @classmethod
    def load(cls, heights: HeightMatrix) -> "Forest":
        height = len(heights)
        width = len(heights[0])
        trees_by_pos: Dict[Tuple[int, int], Tree] = {}
        for i, row in enumerate(heights):
            for j, col in enumerate(row):
                assert (i, j) not in trees_by_pos
                visible: Dict[Direction, Optional[bool]] = {
                    Direction.NORTH: None,
                    Direction.SOUTH: None,
                    Direction.EAST: None,
                    Direction.WEST: None
                }
                tree = Tree(row=i, col=j, height=col)
                if i == 0:
                    tree.set_max_height(-1, Direction.NORTH)
                elif i == height - 1:
                    tree.set_max_height(-1, Direction.SOUTH)
                elif j == 0:
                    tree.set_max_height(-1, Direction.WEST)
                elif j == width - 1:
                    tree.set_max_height(-1, Direction.EAST)
                trees_by_pos[(i, j)] = tree
        for i in range(height):
            for j in range(width):
                tree = trees_by_pos[(i, j)]
                for nrow, ncol, direction in neighborhood(i, j, width, height):
                    tree.add_neighbor(trees_by_pos[(nrow, ncol)], direction)

        return cls([[trees_by_pos[(row, col)] for col in range(width)] for row in range(height)])

    def __str__(self):
        s = ""
        for row in self.trees:
            for tree in row:
                vis = tree.is_visible_from(Direction.NORTH)
                if vis is None:
                    v = " ? "
                elif vis:
                    v = f" ^ "
                else:
                    v = f"   "
                s = f"{s}{v}"
            s = f"{s}\n"
            for tree in row:
                vis = tree.is_visible_from(Direction.WEST)
                if vis is None:
                    w = f"?{tree.height}"
                elif vis:
                    w = f"<{tree.height}"
                else:
                    w = f" {tree.height}"
                vis = tree.is_visible_from(Direction.EAST)
                if vis is None:
                    e = f"?"
                elif vis:
                    e = f">"
                else:
                    e = f" "
                s = f"{s}{w}{e}"
            s = f"{s}\n"
            for tree in row:
                vis = tree.is_visible_from(Direction.SOUTH)
                if vis is None:
                    v = " ? "
                elif vis:
                    v = f" V "
                else:
                    v = f"   "
                s = f"{s}{v}"
            s = f"{s}\n"
        return s


@challenge(day=8)
def visible_trees(path: Path) -> int:
    trees = Forest.load(load(path))
    print(str(trees))
    return sum(1 for t in trees if t.visible)
