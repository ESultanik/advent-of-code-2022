from enum import Enum
from typing import Dict, Iterator, List, Optional, Tuple, Union

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


UnknownTree = object()


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
        self.highest_tree: Dict[Direction, Optional[Union[Tree, UnknownTree]]] = {
            Direction.NORTH: UnknownTree,
            Direction.SOUTH: UnknownTree,
            Direction.EAST: UnknownTree,
            Direction.WEST: UnknownTree
        }

    @property
    def visible(self) -> Optional[bool]:
        if any(t is None or t.height < self.height for t in self.highest_tree.values()):
            return True
        elif all(v is not None and v is not UnknownTree for v in self.highest_tree.values()):
            return False
        else:
            return None

    def is_visible_from(self, direction: Direction) -> Optional[bool]:
        highest = self.highest_tree[direction]
        if highest is UnknownTree:
            return None
        elif highest is None or highest.height < self.height:
            return True
        else:
            return False

    def highest_in_direction(self, direction: Direction) -> "Tree":
        highest = self.highest_tree[direction]
        if highest is not UnknownTree and highest.height > self.height:
            return highest
        else:
            return self

    def set_highest_tree(self, highest_tree: Optional["Tree"], in_direction: Direction):
        existing_highest_tree = self.highest_tree[in_direction]
        if existing_highest_tree == highest_tree:
            return
        # assert existing_highest_tree is UnknownTree
        if highest_tree is None:
            next_highest_tree = self
        else:
            if self.height >= highest_tree.height:
                next_highest_tree = self
            else:
                next_highest_tree = highest_tree
        self.highest_tree[in_direction] = highest_tree
        # print(f"{self!s}.next_highest_tree in {in_direction} = {highest_tree!s};\t"
        #       f"visible = {self.is_visible_from(in_direction)}")
        # propagate the visibility
        neighbor = self._neighbors[in_direction.opposite]
        if neighbor is not None:
            neighbor.set_highest_tree(next_highest_tree, in_direction)

    def add_neighbor(self, tree: "Tree", direction: Direction):
        if self._neighbors[direction] is not None:
            if self._neighbors[direction] is tree:
                return
            raise ValueError()
        self._neighbors[direction] = tree

    def __eq__(self, other):
        return isinstance(other, Tree) and other.row == self.row and other.col == self.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __str__(self):
        return f"🌲({self.row}, {self.col})↑{self.height}"


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

    @property
    def height(self) -> int:
        return len(self.trees)

    @property
    def width(self) -> int:
        return len(self.trees[0])

    def view_distance(self, tree: Tree, in_direction: Direction) -> int:
        highest = tree.highest_tree[in_direction]
        # print(f"Highest for {tree!s} in {in_direction}: {highest!s}")
        if highest is UnknownTree:
            raise ValueError()
        elif highest is None or tree.height > highest.height:
            if in_direction == Direction.EAST:
                return self.width - tree.col - 1
            elif in_direction == Direction.WEST:
                return tree.col
            elif in_direction == Direction.SOUTH:
                return self.height - tree.row - 1
            else:
                return tree.row
        else:
            # do a manual search
            row, col = tree.row, tree.col
            trees = 0
            while True:
                if in_direction == Direction.EAST:
                    col += 1
                elif in_direction == Direction.WEST:
                    col -= 1
                elif in_direction == Direction.SOUTH:
                    row += 1
                else:
                    row -= 1
                if not (0 <= row < self.height and 0 <= col < self.width):
                    break
                h = self.trees[row][col].height
                trees += 1
                if h >= tree.height:
                    break
            return trees

    def scenic_score(self, tree: Tree):
        return self.view_distance(tree, Direction.NORTH) * self.view_distance(tree, Direction.EAST) * \
               self.view_distance(tree, Direction.SOUTH) * self.view_distance(tree, Direction.WEST)

    @classmethod
    def load(cls, heights: HeightMatrix) -> "Forest":
        height = len(heights)
        width = len(heights[0])
        trees_by_pos: Dict[Tuple[int, int], Tree] = {}
        for i, row in enumerate(heights):
            for j, col in enumerate(row):
                assert (i, j) not in trees_by_pos
                tree = Tree(row=i, col=j, height=col)
                trees_by_pos[(i, j)] = tree
        for i in range(height):
            for j in range(width):
                tree = trees_by_pos[(i, j)]
                for nrow, ncol, direction in neighborhood(i, j, width, height):
                    tree.add_neighbor(trees_by_pos[(nrow, ncol)], direction)
        for i in range(height):
            for j in range(width):
                tree = trees_by_pos[(i, j)]
                if i == 0:
                    tree.set_highest_tree(None, Direction.NORTH)
                if i == height - 1:
                    tree.set_highest_tree(None, Direction.SOUTH)
                if j == 0:
                    tree.set_highest_tree(None, Direction.WEST)
                if j == width - 1:
                    tree.set_highest_tree(None, Direction.EAST)

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
    # print(str(trees))
    return sum(1 for t in trees if t.visible)


"""
--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390
Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390
Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
"""


@challenge(day=8)
def scenic_score(path: Path) -> int:
    trees = Forest.load(load(path))
    # print(str(trees))
    return max(trees.scenic_score(tree) for tree in trees)
