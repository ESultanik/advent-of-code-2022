"""
--- Day 22: Monkey Map ---
The monkeys take you on a surprisingly easy trail through the jungle. They're even going in roughly the right direction according to your handheld device's Grove Positioning System.

As you walk, the monkeys explain that the grove is protected by a force field. To pass through the force field, you have to enter a password; doing so involves tracing a specific path on a strangely-shaped board.

At least, you're pretty sure that's what you have to do; the elephants aren't exactly fluent in monkey.

The monkeys give you notes that they took when they last saw the password entered (your puzzle input).

For example:

        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
The first half of the monkeys' notes is a map of the board. It is comprised of a set of open tiles (on which you can move, drawn .) and solid walls (tiles which you cannot enter, drawn #).

The second half is a description of the path you must follow. It consists of alternating numbers and letters:

A number indicates the number of tiles to move in the direction you are facing. If you run into a wall, you stop moving forward and continue with the next instruction.
A letter indicates whether to turn 90 degrees clockwise (R) or counterclockwise (L). Turning happens in-place; it does not change your current tile.
So, a path like 10R5 means "go forward 10 tiles, then turn clockwise 90 degrees, then go forward 5 tiles".

You begin the path in the leftmost open tile of the top row of tiles. Initially, you are facing to the right (from the perspective of how the map is drawn).

If a movement instruction would take you off of the map, you wrap around to the other side of the board. In other words, if your next tile is off of the board, you should instead look in the direction opposite of your current facing as far as you can until you find the opposite edge of the board, then reappear there.

For example, if you are at A and facing to the right, the tile in front of you is marked B; if you are at C and facing down, the tile in front of you is marked D:

        ...#
        .#..
        #...
        ....
...#.D.....#
........#...
B.#....#...A
.....C....#.
        ...#....
        .....#..
        .#......
        ......#.
It is possible for the next tile (after wrapping around) to be a wall; this still counts as there being a wall in front of you, and so movement stops before you actually wrap to the other side of the board.

By drawing the last facing you had with an arrow on each tile you visit, the full path taken by the above example looks like this:

        >>v#
        .#v.
        #.v.
        ..v.
...#...v..v#
>>>v...>#.>>
..#v...#....
...>>>>v..#.
        ...#....
        .....#..
        .#......
        ......#.
To finish providing the password to this strange input device, you need to determine numbers for your final row, column, and facing as your final position appears from the perspective of the original map. Rows start from 1 at the top and count downward; columns start from 1 at the left and count rightward. (In the above example, row 1, column 1 refers to the empty space with no tile on it in the top-left corner.) Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^). The final password is the sum of 1000 times the row, 4 times the column, and the facing.

In the above example, the final row is 6, the final column is 8, and the final facing is 0. So, the final password is 1000 * 6 + 4 * 8 + 0: 6032.

Follow the path given in the monkeys' notes. What is the final password?
"""

from abc import ABC, abstractmethod
from enum import Enum
from functools import lru_cache
from typing import Dict, Iterable, Iterator, List, Mapping, Optional, Tuple

from . import challenge, Path


class Space(Enum):
    EMPTY = "."
    WALL = "#"
    OUTSIDE = " "

    @staticmethod
    def parse(s: str) -> "Space":
        for space in Space:
            if space.value == s:
                return space
        raise ValueError(f"No such space: {s!r}")


class Facing(Enum):
    EAST = (0, ">", 0, 1)
    SOUTH = (1, "v", 1, 0)
    WEST = (2, "<", 0, -1)
    NORTH = (3, "^", -1, 0)

    def __init__(self, password: int, symbol: str, row_delta: int, col_delta: int):
        self.password: int = password
        self.symbol: str = symbol
        self.row_delta: int = row_delta
        self.col_delta: int = col_delta

    def __str__(self):
        return self.symbol


class Map:
    def __init__(self, rows: Iterable[Mapping[int, Space]]):
        self.rows: List[Dict[int, Space]] = [
            {
                col: space
                for col, space in row.items()
                if space != Space.OUTSIDE
            }
            for row in rows
        ]

    @property
    def starting_col(self) -> int:
        return min(self.rows[0].keys())

    def get(self, row: int, col: int) -> Space:
        if row < 0 or row >= len(self.rows) or col not in self.rows[row]:
            return Space.OUTSIDE
        else:
            return self.rows[row][col]

    @lru_cache(maxsize=10000000)
    def wraps_to(self, row: int, col: int, facing: Facing) -> Tuple[int, int, Facing]:
        row += facing.row_delta
        col += facing.col_delta
        assert self.get(row, col) == Space.OUTSIDE
        # move in the opposite direction and return the last non-outside cell before going outside
        while True:
            row -= facing.row_delta
            col -= facing.col_delta
            if self.get(row, col) == Space.OUTSIDE:
                # we got to the other side, so move back inside
                row += facing.row_delta
                col += facing.col_delta
                break
        return row, col, facing

    @property
    def width(self) -> int:
        return max(
            max(row.keys())
            for row in self.rows
        ) + 1

    def __str__(self):
        return "\n".join((
            "".join((
                self.get(row, col).value
                for col in range(self.width)
            ))
            for row in range(len(self.rows))
        ))


class State:
    def __init__(
            self, board: Map, row: Optional[int] = None, col: Optional[int] = None, facing: Facing = Facing.EAST
    ):
        self.board: Map = board
        if row is None or col is None:
            self.row: int = 0
            self.col: int = board.starting_col
        else:
            self.row = row
            self.col = col
        self.facing: Facing = facing

    @property
    def password(self) -> int:
        return 1000 * (self.row + 1) + 4 * (self.col + 1) + self.facing.password


class Move(ABC):
    @abstractmethod
    def apply(self, state: State) -> State:
        raise NotImplementedError()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()

    @classmethod
    def parse(cls, moves: str) -> Iterator["Move"]:
        moves = moves.strip()
        while moves:
            if moves[0] == "R":
                yield TurnClockwise()
                moves = moves[1:]
            elif moves[0] == "L":
                yield TurnCounterClockwise()
                moves = moves[1:]
            else:
                number = ""
                while moves and ord("0") <= ord(moves[0]) <= ord("9"):
                    number = f"{number}{moves[0]}"
                    moves = moves[1:]
                if not number:
                    raise ValueError(f"Unexpected move: {moves!r}")
                yield MoveForward(int(number))


class MoveForward(Move):
    def __init__(self, distance: int):
        self.distance: int = distance

    def apply(self, state: State) -> State:
        for _ in range(self.distance):
            new_row = state.row + state.facing.row_delta
            new_col = state.col + state.facing.col_delta
            new_facing = state.facing
            next_space = state.board.get(new_row, new_col)
            if next_space == Space.OUTSIDE:
                # wrap around
                new_row, new_col, new_facing = state.board.wraps_to(state.row, state.col, new_facing)
                next_space = state.board.get(new_row, new_col)
            if next_space == Space.WALL:
                # we hit a wall, so stop
                break
            state = State(board=state.board, row=new_row, col=new_col, facing=new_facing)
        return state

    def __str__(self):
        return str(self.distance)


class TurnClockwise(Move):
    def apply(self, state: State) -> State:
        if state.facing == Facing.EAST:
            new_heading = Facing.SOUTH
        elif state.facing == Facing.SOUTH:
            new_heading = Facing.WEST
        elif state.facing == Facing.WEST:
            new_heading = Facing.NORTH
        else:
            assert state.facing == Facing.NORTH
            new_heading = Facing.EAST
        return State(board=state.board, row=state.row, col=state.col, facing=new_heading)

    def __str__(self):
        return "R"


class TurnCounterClockwise(Move):
    def apply(self, state: State) -> State:
        if state.facing == Facing.EAST:
            new_heading = Facing.NORTH
        elif state.facing == Facing.NORTH:
            new_heading = Facing.WEST
        elif state.facing == Facing.WEST:
            new_heading = Facing.SOUTH
        else:
            assert state.facing == Facing.SOUTH
            new_heading = Facing.EAST
        return State(board=state.board, row=state.row, col=state.col, facing=new_heading)

    def __str__(self):
        return "L"


def load(path: Path) -> Tuple[Map, List[Move]]:
    rows: List[Dict[int, Space]] = []
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip()
            if not line:
                break
            rows.append({
                col: Space.parse(s)
                for col, s in enumerate(line)
            })
        for line in f:
            moves = list(Move.parse(line.strip()))
            break
    return Map(rows), moves


@challenge(day=22)
def final_password(path: Path) -> int:
    m, moves = load(path)
    state = State(m)
    for move in moves:
        state = move.apply(state)
    return state.password


"""
--- Part Two ---
As you reach the force field, you think you hear some Elves in the distance. Perhaps they've already arrived?

You approach the strange input device, but it isn't quite what the monkeys drew in their notes. Instead, you are met with a large cube; each of its six faces is a square of 50x50 tiles.

To be fair, the monkeys' map does have six 50x50 regions on it. If you were to carefully fold the map, you should be able to shape it into a cube!

In the example above, the six (smaller, 4x4) faces of the cube are:

        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666
You still start in the same position and with the same facing as before, but the wrapping rules are different. Now, if you would walk off the board, you instead proceed around the cube. From the perspective of the map, this can look a little strange. In the above example, if you are at A and move to the right, you would arrive at B facing down; if you are at C and move down, you would arrive at D facing up:

        ...#
        .#..
        #...
        ....
...#.......#
........#..A
..#....#....
.D........#.
        ...#..B.
        .....#..
        .#......
        ..C...#.
Walls still block your path, even if they are on a different face of the cube. If you are at E facing up, your movement is blocked by the wall marked by the arrow:

        ...#
        .#..
     -->#...
        ....
...#..E....#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.
Using the same method of drawing the last facing you had with an arrow on each tile you visit, the full path taken by the above example now looks like this:

        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#..^...v#    
.>>>>>^.#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#.
The final password is still calculated from your final position and facing from the perspective of the map. In this example, the final row is 5, the final column is 7, and the final facing is 3, so the final password is 1000 * 5 + 4 * 7 + 3 = 5031.

Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?
"""


class Cube(Map):
    def __init__(self, board: Map):
        initial_empty = min(board.rows[0].keys())
        if initial_empty % 2 != 0:
            raise ValueError(f"{initial_empty} is not even")
        self.dimension: int = initial_empty // 2
        for row in range(self.dimension):
            if (
                    min(board.rows[row].keys()) != initial_empty
                    or
                    max(board.rows[row].keys()) + 1 != self.dimension * 3
            ):
                raise ValueError(f"Invalid row for a {self.dimension}x{self.dimension} cube: {board.rows[row]!r}")
        for row in range(self.dimension, self.dimension * 2):
            if (
                    min(board.rows[row].keys()) != 0
                    or
                    max(board.rows[row].keys()) + 1 != self.dimension * 3
            ):
                raise ValueError(f"Invalid row for a {self.dimension}x{self.dimension} cube: {board.rows[row]!r}")
        for row in range(self.dimension * 2, self.dimension * 3):
            if (
                    min(board.rows[row].keys()) != initial_empty
                    or
                    max(board.rows[row].keys()) + 1 != self.dimension * 4
            ):
                raise ValueError(f"Invalid row for a {self.dimension}x{self.dimension} cube: {board.rows[row]!r}")
        super().__init__(board.rows)

    def face(self, row: int, col: int) -> int:
        if row < self.dimension and self.dimension * 2 <= col < self.dimension * 3:
            face = 1
        elif col < self.dimension <= row < self.dimension * 2:
            face = 2
        elif col < self.dimension * 2 and self.dimension <= row < self.dimension * 2:
            face = 3
        elif col < self.dimension * 3 and self.dimension <= row < self.dimension * 2:
            face = 4
        elif self.dimension * 2 <= col < self.dimension * 3 and self.dimension * 2 <= row < self.dimension * 3:
            face = 5
        elif self.dimension * 2 <= row < self.dimension * 3 <= col < self.dimension * 4:
            face = 6
        else:
            raise ValueError(f"<row={row}, col={col}> is not on the cube!")
        return face

    @lru_cache(maxsize=10000000)
    def wraps_to(self, row: int, col: int, facing: Facing) -> Tuple[int, int, Facing]:
        face = self.face(row, col)
        if face == 1:
            if facing == Facing.WEST:
                # moving to face 3
                facing = Facing.SOUTH
                col = self.dimension + row
                row = self.dimension
                assert self.face(row, col) == 3
            elif facing == Facing.NORTH:
                # moving to face 2
                facing = Facing.SOUTH
                col = self.dimension - (col - self.dimension * 2) - 1
                row = self.dimension
                assert self.face(row, col) == 2
            elif facing == Facing.EAST:
                # move to face 6
                facing = Facing.WEST
                row = self.dimension * 3 - row - 1
                col = self.dimension * 4 - 1
                assert self.face(row, col) == 6
            else:
                raise ValueError("This should never happen")
        elif face == 2:
            if facing == Facing.NORTH:
                # moving to face 1
                facing = Facing.SOUTH
                col = self.dimension * 2 + (self.dimension - col - 1)
                row = 0
                assert self.face(row, col) == 1
            elif facing == Facing.WEST:
                # moving to face 6
                facing = Facing.NORTH
                col = self.dimension * 4 - (row - self.dimension) - 1
                row = self.dimension * 3 - 1
                assert self.face(row, col) == 6
            elif facing == Facing.SOUTH:
                # moving to face 5
                facing = Facing.NORTH
                col = self.dimension * 2 + (self.dimension - col - 1)
                row = self.dimension * 3 - 1
                assert self.face(row, col) == 5
            else:
                raise ValueError("This should never happen")
        elif face == 3:
            if facing == Facing.NORTH:
                # moving to face 1
                facing = Facing.EAST
                row = col - self.dimension
                col = self.dimension * 2
                assert self.face(row, col) == 1
            elif facing == Facing.SOUTH:
                # moving to face 5
                facing = Facing.EAST
                row = self.dimension * 2 + (self.dimension - (col - self.dimension))
                col = self.dimension * 2
                assert self.face(row, col) == 5
            else:
                raise ValueError("This should never happen")
        elif face == 4:
            if facing == Facing.EAST:
                # moving to face 6
                facing = Facing.SOUTH
                col = self.dimension * 4 - (row - self.dimension) - 1
                row = self.dimension * 2
                assert self.face(row, col) == 6
            else:
                raise ValueError("This should never happen")
        elif face == 5:
            if facing == Facing.WEST:
                # moving to face 3
                facing = Facing.NORTH
                col = self.dimension * 2 - (row - self.dimension * 2) - 1
                row = self.dimension * 2 - 1
                assert self.face(row, col) == 3
            elif facing == Facing.SOUTH:
                # moving to face 2
                facing = Facing.NORTH
                col = self.dimension - (col - self.dimension * 2) - 1
                row = self.dimension * 2 - 1
                assert self.face(row, col) == 2
            else:
                raise ValueError("This should never happen")
        elif face == 6:
            if facing == Facing.NORTH:
                # moving to face 4
                facing = Facing.WEST
                row = self.dimension + (self.dimension - (col - self.dimension * 3))
                col = self.dimension * 3 - 1
                assert self.face(row, col) == 4
            elif facing == Facing.EAST:
                # moving to face 1
                facing = Facing.WEST
                row = self.dimension - (col - self.dimension * 3) - 1
                col = self.dimension * 3 - 1
                assert self.face(row, col) == 1
            elif facing == Facing.SOUTH:
                # moving to face 2
                facing = Facing.EAST
                row = self.dimension * 2 - (col - self.dimension * 3) - 1
                col = 0
                assert self.face(row, col) == 2
            else:
                raise ValueError("This should never happen")
        else:
            raise NotImplementedError()
        return row, col, facing


@challenge(day=22)
def cube_folding(path: Path) -> int:
    m, moves = load(path)
    cube = Cube(m)
    state = State(cube)
    rows: List[List[str]] = [list(row) for row in str(cube).split("\n")]
    rows[state.row][state.col] = state.facing.symbol
    for move in moves:
        state = move.apply(state)
        rows[state.row][state.col] = state.facing.symbol
    print("\n".join((
        "".join(row)
        for row in rows
    )))
    return state.password
