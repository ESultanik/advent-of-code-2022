"""
--- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?
"""

from enum import Enum
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from . import challenge, Path


class Space(Enum):
    AIR = "."
    ROCK = "#"
    SAND = "o"


class CaveRow:
    def __init__(self, cave: "Cave", row: int):
        self.cave: Cave = cave
        self.row: int = row

    def __getitem__(self, col_index: int) -> Space:
        if self.cave.floor_row is not None and self.row >= self.cave.floor_row:
            return Space.ROCK
        elif self.row not in self.cave.cave:
            return Space.AIR
        row_dict = self.cave.cave[self.row]
        if col_index not in row_dict:
            return Space.AIR
        else:
            return row_dict[col_index]

    def __setitem__(self, col_index: int, value: Space):
        if self.cave.floor_row is not None and self.row >= self.cave.floor_row:
            raise ValueError(f"Cannot change the value at or below the floor of {self.cave.floor_row}!")
        elif self.row not in self.cave.cave:
            row_dict = {}
            self.cave.cave[self.row] = row_dict
        else:
            row_dict = self.cave.cave[self.row]
        row_dict[col_index] = value


class Cave:
    def __init__(self, cave: Dict[int, Dict[int, Space]]):
        self.cave: Dict[int, Dict[int, Space]] = {
            row_index: {
                col_index: col
                for col_index, col in row.items()
            }
            for row_index, row in cave.items()
        }
        self.min_row: int = 0
        self.sand_row: int = 0
        self.sand_col: int = 500
        self.floor_row: Optional[int] = None

    @property
    def max_row(self) -> int:
        return max(self.cave.keys())

    @property
    def min_col(self) -> int:
        return min(c for r in self.cave.values() for c in r)

    @property
    def max_col(self) -> int:
        return max(c for r in self.cave.values() for c in r)

    def __getitem__(self, row_index: int) -> CaveRow:
        return CaveRow(cave=self, row=row_index)

    @classmethod
    def load(cls, paths: Iterable[Iterable[Tuple[int, int]]]) -> "Cave":
        cave: Dict[int, Dict[int, Space]] = {}
        for path in paths:
            last_row: Optional[int] = None
            last_col: Optional[int] = None
            for col, row in path:
                if last_row is not None and last_col is not None:
                    if last_row == row:
                        if last_col < col:
                            from_col = last_col
                            to_col = col
                        else:
                            from_col = col
                            to_col = last_col
                        for c in range(from_col, to_col + 1):
                            if row not in cave:
                                cave[row] = {c: Space.ROCK}
                            else:
                                cave[row][c] = Space.ROCK
                    elif last_col == col:
                        if last_row < row:
                            from_row = last_row
                            to_row = row
                        else:
                            from_row = row
                            to_row = last_row
                        for r in range(from_row, to_row + 1):
                            if r not in cave:
                                cave[r] = {col: Space.ROCK}
                            else:
                                cave[r][col] = Space.ROCK
                last_row, last_col = row, col
        return cls(cave)

    def drop_sand(self) -> Tuple[int, int]:
        sand_row = self.sand_row
        sand_col = self.sand_col
        max_row = self.max_row
        while sand_row <= max_row:
            next_row = self[sand_row + 1]
            if next_row[sand_col] != Space.AIR:
                if next_row[sand_col - 1] != Space.AIR:
                    if next_row[sand_col + 1] != Space.AIR:
                        return sand_row, sand_col
                    else:
                        sand_row += 1
                        sand_col += 1
                else:
                    sand_row += 1
                    sand_col -= 1
            else:
                sand_row += 1
        return sand_row, sand_col

    def simulate(self) -> Iterator[Tuple[int, int]]:
        while True:
            sand_row, sand_col = self.drop_sand()
            if self.floor_row is None and sand_row > self.max_row:
                break
            self[sand_row][sand_col] = Space.SAND
            yield sand_row, sand_col
            if sand_row == self.sand_row and sand_col == self.sand_col:
                break

    def __str__(self):
        min_col = self.min_col
        max_col = self.max_col
        rows: List[str] = []
        for row in range(self.min_row, self.max_row + 1):
            s_row: List[str] = []
            for col in range(min_col, max_col + 1):
                if row == self.sand_row and col == self.sand_col:
                    s_row.append("+")
                else:
                    s_row.append(self[row][col].value)  # type: ignore
            rows.append("".join(s_row))
        return "\n".join(rows)


def load(path: Path) -> Cave:
    with open(path, "r") as f:
        cave: Iterable[Iterable[Tuple[int, int]]] = [
            [
                tuple(map(int, p.split(",")))
                for p in line.strip().split(" -> ")
            ]
            for line in f
        ]
        return Cave.load(cave)


@challenge(day=14)
def units_of_resting_sand(path: Path) -> int:
    cave = load(path)
    sand_dropped = sum(1 for _ in cave.simulate())
    print(str(cave))
    return sand_dropped


"""
--- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
"""


@challenge(day=14)
def units_of_resting_sand(path: Path) -> int:
    cave = load(path)
    cave.floor_row = cave.max_row + 2
    sand_dropped = sum(1 for _ in cave.simulate())
    print(str(cave))
    return sand_dropped
