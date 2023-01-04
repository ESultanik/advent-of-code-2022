"""
--- Day 23: Unstable Diffusion ---
You enter a large crater of gray dirt where the grove is supposed to be. All around you, plants you imagine were expected to be full of fruit are instead withered and broken. A large group of Elves has formed in the middle of the grove.

"...but this volcano has been dormant for months. Without ash, the fruit can't grow!"

You look up to see a massive, snow-capped mountain towering above you.

"It's not like there are other active volcanoes here; we've looked everywhere."

"But our scanners show active magma flows; clearly it's going somewhere."

They finally notice you at the edge of the grove, your pack almost overflowing from the random star fruit you've been collecting. Behind you, elephants and monkeys explore the grove, looking concerned. Then, the Elves recognize the ash cloud slowly spreading above your recent detour.

"Why do you--" "How is--" "Did you just--"

Before any of them can form a complete question, another Elf speaks up: "Okay, new plan. We have almost enough fruit already, and ash from the plume should spread here eventually. If we quickly plant new seedlings now, we can still make it to the extraction point. Spread out!"

The Elves each reach into their pack and pull out a tiny plant. The plants rely on important nutrients from the ash, so they can't be planted too close together.

There isn't enough time to let the Elves figure out where to plant the seedlings themselves; you quickly scan the grove (your puzzle input) and note their positions.

For example:

....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
The scan shows Elves # and empty ground .; outside your scan, more empty ground extends a long way in every direction. The scan is oriented so that north is up; orthogonal directions are written N (north), S (south), W (west), and E (east), while diagonal directions are written NE, NW, SE, SW.

The Elves follow a time-consuming process to figure out where they should each go; you can speed up this process considerably. The process consists of some number of rounds during which Elves alternate between considering where to move and actually moving.

During the first half of each round, each Elf considers the eight positions adjacent to themself. If no other Elves are in one of those eight positions, the Elf does not do anything during this round. Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:

If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
After each Elf has had a chance to propose a move, the second half of the round can begin. Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose moving to that position. If two or more Elves propose moving to the same position, none of those Elves move.

Finally, at the end of the round, the first direction the Elves considered is moved to the end of the list of directions. For example, during the second round, the Elves would try proposing a move to the south first, then west, then east, then north. On the third round, the Elves would first consider west, then east, then north, then south.

As a smaller example, consider just these five Elves:

.....
..##.
..#..
.....
..##.
.....
The northernmost two Elves and southernmost two Elves all propose moving north, while the middle Elf cannot move north and proposes moving south. The middle Elf proposes the same destination as the southwest Elf, so neither of them move, but the other three do:

..##.
.....
..#..
...#.
..#..
.....
Next, the northernmost two Elves and the southernmost Elf all propose moving south. Of the remaining middle two Elves, the west one cannot move south and proposes moving west, while the east one cannot move south or west and proposes moving east. All five Elves succeed in moving to their proposed positions:

.....
..##.
.#...
....#
.....
..#..
Finally, the southernmost two Elves choose not to move at all. Of the remaining three Elves, the west one proposes moving west, the east one proposes moving east, and the middle one proposes moving north; all three succeed in moving:

..#..
....#
#....
....#
.....
..#..
At this point, no Elves need to move, and so the process ends.

The larger example above proceeds as follows:

== Initial State ==
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............

== End of Round 1 ==
..............
.......#......
.....#...#....
...#..#.#.....
.......#..#...
....#.#.##....
..#..#.#......
..#.#.#.##....
..............
....#..#......
..............
..............

== End of Round 2 ==
..............
.......#......
....#.....#...
...#..#.#.....
.......#...#..
...#..#.#.....
.#...#.#.#....
..............
..#.#.#.##....
....#..#......
..............
..............

== End of Round 3 ==
..............
.......#......
.....#....#...
..#..#...#....
.......#...#..
...#..#.#.....
.#..#.....#...
.......##.....
..##.#....#...
...#..........
.......#......
..............

== End of Round 4 ==
..............
.......#......
......#....#..
..#...##......
...#.....#.#..
.........#....
.#...###..#...
..#......#....
....##....#...
....#.........
.......#......
..............

== End of Round 5 ==
.......#......
..............
..#..#.....#..
.........#....
......##...#..
.#.#.####.....
...........#..
....##..#.....
..#...........
..........#...
....#..#......
..............
After a few more rounds...

== End of Round 10 ==
.......#......
...........#..
..#.#..#......
......#.......
...#.....#..#.
.#......##....
.....##.......
..#........#..
....#.#..#....
..............
....#..#..#...
..............
To make sure they're on the right track, the Elves like to check after round 10 that they're making good progress toward covering enough ground. To do this, count the number of empty ground tiles contained by the smallest rectangle that contains every Elf. (The edges of the rectangle should be aligned to the N/S/E/W directions; the Elves do not have the patience to calculate arbitrary rectangles.) In the above example, that rectangle is:

......#.....
..........#.
.#.#..#.....
.....#......
..#.....#..#
#......##...
....##......
.#........#.
...#.#..#...
............
...#..#..#..
In this region, the number of empty ground tiles is 110.

Simulate the Elves' process and find the smallest rectangle that contains the Elves after 10 rounds. How many empty ground tiles does that rectangle contain?
"""

from collections import defaultdict
from enum import Enum
from itertools import chain
from typing import Dict, Iterable, Iterator, List, Set, Tuple

from . import challenge, Path


Position = Tuple[int, int]


class Grove:
    def __init__(self, elf_positions: Iterable[Position]):
        self._elves: Dict[int, Set[int]] = {}
        for row, col in elf_positions:
            if row not in self._elves:
                self._elves[row] = {col}
            else:
                self._elves[row].add(col)

    def is_ground(self, row: int, col: int) -> bool:
        return row not in self._elves or col not in self._elves[row]

    def __iter__(self) -> Iterator[Position]:
        for row, r in self._elves.items():
            yield from ((row, col) for col in r)

    def __len__(self):
        return sum(len(r) for r in self._elves.values())

    @classmethod
    def load(cls, path: Path) -> "Grove":
        with open(path, "r") as f:
            return cls((
                (row, col)
                for row, line in enumerate(f)
                for col, c in enumerate(line)
                if c == "#"
            ))

    @property
    def min_row(self) -> int:
        return min(self._elves.keys())

    @property
    def max_row(self) -> int:
        return max(self._elves.keys())

    @property
    def min_col(self) -> int:
        return min(
            min(r)
            for r in self._elves.values()
        )

    @property
    def max_col(self) -> int:
        return max(
            max(r)
            for r in self._elves.values()
        )

    @property
    def width(self) -> int:
        return self.max_col - self.min_col + 1

    @property
    def height(self) -> int:
        return self.max_row - self.min_row + 1

    def empty_tiles(self) -> int:
        return self.width * self.height - len(self)

    def __str__(self):
        min_col, max_col = self.min_col, self.max_col
        rows: List[str] = []
        for row in range(self.min_row, self.max_row + 1):
            rows.append(
                "".join((
                    ["#", "."][self.is_ground(row, col)]
                    for col in range(min_col, max_col + 1)
                ))
            )
        return "\n".join(rows)


class Direction(Enum):
    NORTH = -1, 0
    SOUTH = 1, 0
    EAST = 0, 1
    WEST = 0, -1
    NE = -1, 1
    NW = -1, -1
    SE = 1, 1
    SW = 1, -1

    def __init__(self, row_delta: int, col_delta: int):
        self.row_delta: int = row_delta
        self.col_delta: int = col_delta

    @property
    def neighborhood(self) -> Tuple["Direction", ...]:
        match self:
            case Direction.NORTH:
                return Direction.NORTH, Direction.NE, Direction.NW
            case Direction.SOUTH:
                return Direction.SOUTH, Direction.SE, Direction.SW
            case Direction.WEST:
                return Direction.WEST, Direction.NW, Direction.SW
            case Direction.EAST:
                return Direction.EAST, Direction.NE, Direction.SE
            case _:
                raise NotImplementedError(str(self))


class Round:
    def __init__(
            self,
            grove: Grove,
            directions: Iterable[Direction] = (Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST)
    ):
        self.grove: Grove = grove
        self.directions: Tuple[Direction, ...] = tuple(directions)

    def next(self) -> "Round":
        proposals: Dict[Position, Set[Position]] = defaultdict(set)
        for row, col in self.grove:
            is_ground = {
                d: self.grove.is_ground(row + d.row_delta, col + d.col_delta)
                for d in Direction
            }
            if all(is_ground.values()):
                # all surrounding positions are ground, so do not propose anything
                continue
            for d in self.directions:
                if all(is_ground[n] for n in d.neighborhood):
                    proposals[(row + d.row_delta, col + d.col_delta)].add((row, col))
                    break
        # move the elves
        to_move: Dict[Position, Position] = {
            next(iter(from_positions)): to_pos
            for to_pos, from_positions in proposals.items()
            if len(from_positions) == 1
        }
        unmoved: Set[Position] = {p for p in self.grove if p not in to_move}
        next_directions = self.directions[1:] + (self.directions[0],)
        return Round(Grove(chain(to_move.values(), unmoved)), next_directions)


@challenge(day=23)
def empty_ground_tiles(path: Path) -> int:
    grove = Grove.load(path)
    r = Round(grove)
    for _ in range(10):
        r = r.next()
    print(str(r.grove))
    return r.grove.empty_tiles()
