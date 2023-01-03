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
    def wraps_to(self, row: int, col: int, facing: Facing) -> Tuple[int, int]:
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
        return row, col

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
            next_space = state.board.get(new_row, new_col)
            if next_space == Space.OUTSIDE:
                # wrap around
                new_row, new_col = state.board.wraps_to(new_row, new_col, state.facing)
                next_space = state.board.get(new_row, new_col)
            if next_space == Space.WALL:
                # we hit a wall, so stop
                break
            state = State(board=state.board, row=new_row, col=new_col, facing=state.facing)
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
