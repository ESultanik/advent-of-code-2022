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
from math import isqrt
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

    @property
    def opposite(self) -> "Facing":
        match self:
            case Facing.EAST:
                return Facing.WEST
            case Facing.WEST:
                return Facing.EAST
            case Facing.NORTH:
                return Facing.SOUTH
            case Facing.SOUTH:
                return Facing.NORTH

    def rotate_clockwise(self, n: int = 1) -> "Facing":
        f = self
        while n % 4 > 0:
            match f:
                case Facing.EAST:
                    f = Facing.SOUTH
                case Facing.WEST:
                    f = Facing.NORTH
                case Facing.SOUTH:
                    f = Facing.WEST
                case Facing.NORTH:
                    f = Facing.EAST
            n -= 1
        return f

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


class Transform(ABC):
    @abstractmethod
    def transform(self, row: int, col: int) -> Tuple[int, int]:
        raise NotImplementedError()

    def __add__(self, addend: "Transform") -> "AffineTransform":
        return AffineTransform(self, addend)


class Rotation(Transform):
    def __init__(self, face: "Face", degrees_clockwise: int):
        if degrees_clockwise % 90 != 0:
            raise ValueError("Rotation must be a multiple of 90 degrees!")
        self.face: Face = face
        self.degrees_clockwise: int = degrees_clockwise

    def transform(self, row: int, col: int) -> Tuple[int, int]:
        if self.degrees_clockwise % 360 == 0:
            return row, col
        row_offset = row - self.face.row
        col_offset = col - self.face.col
        new_row, new_col = self.face.row, self.face.col
        if self.degrees_clockwise % 270 == 0:
            new_row += self.face.cube.dimension - 1 - col_offset
            new_col += row_offset
        elif self.degrees_clockwise % 180 == 0:
            new_row += self.face.cube.dimension - 1 - row_offset
            new_col += self.face.cube.dimension - 1 - col_offset
        else:
            assert self.degrees_clockwise % 90 == 0
            new_row += col_offset
            new_col += self.face.cube.dimension - 1 - row_offset
        return new_row, new_col


class AffineTransform(Transform):
    def __init__(self, *transforms: Transform):
        self.transforms: Tuple[Transform, ...] = tuple(transforms)

    def transform(self, row: int, col: int) -> Tuple[int, int]:
        for t in self.transforms:
            row, col = t.transform(row, col)
        return row, col


class Translation(Transform):
    def __init__(self, row_delta: int, col_delta: int):
        self.row_delta: int = row_delta
        self.col_delta: int = col_delta

    def transform(self, row: int, col: int) -> Tuple[int, int]:
        return row + self.row_delta, col + self.col_delta


class Face:
    def __init__(self, cube: "Cube", row: int, col: int):
        self.cube: Cube = cube
        self.row: int = row
        self.col: int = col
        self.neighbors: Dict[Facing, Tuple[Facing, Face]] = {}

    def __eq__(self, other):
        return isinstance(other, Face) and other.cube.dimension == self.cube.dimension and other.row == self.row and \
            other.col == self.col

    def __hash__(self):
        return hash((self.cube.dimension, self.row, self.col))

    def transform_to_meet(self, neighbor: Facing) -> Transform:
        if neighbor not in self.neighbors:
            raise ValueError(f"There is no neighbor facing {neighbor}")
        neighbor_edge, n = self.neighbors[neighbor]
        rotation = 0
        desired_edge = neighbor_edge.opposite
        while neighbor != desired_edge:
            rotation += 1
            neighbor = neighbor.rotate_clockwise(1)
        translate_to_row = n.row
        translate_to_col = n.col
        match neighbor_edge:
            case Facing.NORTH:
                translate_to_row -= n.cube.dimension
            case Facing.SOUTH:
                translate_to_row += n.cube.dimension
            case Facing.EAST:
                translate_to_col += n.cube.dimension
            case Facing.WEST:
                translate_to_col -= n.cube.dimension
        row_delta = translate_to_row - self.row
        col_delta = translate_to_col - self.col
        return AffineTransform(Rotation(self, rotation * 90), Translation(row_delta, col_delta))

    def get_neighbor_edge(self, neighbor: Facing, map_direction: Facing) -> Tuple[Optional[Facing], Optional["Face"]]:
        if neighbor not in self.neighbors:
            return None, None
        neighbor_edge, n = self.neighbors[neighbor]
        rotation = 0
        desired_edge = neighbor.opposite
        while neighbor_edge != desired_edge:
            rotation += 1
            neighbor_edge = neighbor_edge.rotate_clockwise(1)
        rotated_facing = map_direction.rotate_clockwise(-rotation)
        return rotated_facing, n

    def add_neighbor(self, edge: Facing, neighbor: "Face", neighbor_edge: Optional[Facing] = None):
        if neighbor_edge is None:
            neighbor_edge = edge.opposite
        if edge in self.neighbors:
            if self.neighbors[edge] == (neighbor_edge, neighbor):
                # the face was already added
                return
            raise ValueError(edge)
        elif any(f == neighbor for _, f in self.neighbors.items()):
            raise ValueError(neighbor)
        # add the new neighbor:
        self.neighbors[edge] = neighbor_edge, neighbor
        neighbor.add_neighbor(neighbor_edge, self, edge)
        # propagate this to any of our preexisting neighbors
        for other_neighbor_direction in set(Facing) - {edge, edge.opposite}:
            ne, n = self.get_neighbor_edge(other_neighbor_direction, edge)
            if ne is None or n is None:
                continue
            me, _ = self.get_neighbor_edge(edge, other_neighbor_direction)
            assert me is not None
            n.add_neighbor(ne, neighbor, me)

    def contains(self, row: int, col: int) -> bool:
        return self.row <= row < self.row + self.cube.dimension and self.col <= col < self.col + self.cube.dimension

    def wraps_to(self, row: int, col: int, facing: Facing) -> Tuple[int, int, Facing]:
        if not self.contains(row, col):
            raise ValueError(f"<row={row}, col={col}> is not on this face!")
        elif facing not in self.neighbors:
            raise ValueError(f"<row={row}, col={col}> with facing {facing.symbol} does not wrap!")
        transform = self.transform_to_meet(facing)
        next_row, next_col = row + facing.row_delta, col + facing.col_delta
        trow, tcol = transform.transform(next_row, next_col)
        neighbor_edge, neighbor = self.neighbors[facing]
        assert neighbor.contains(trow, tcol)
        return trow, tcol, neighbor_edge.opposite


class Cube(Map):
    def __init__(self, board: Map):
        total_spots = sum(len(row.keys()) for row in board.rows)
        if total_spots % 6 != 0:
            raise ValueError(f"The total number of spots, {total_spots}, is not divisible by 6!")
        spots_per_face = total_spots // 6
        self.dimension: int = isqrt(spots_per_face)
        if (self.dimension ** 2) * 6 != total_spots:
            raise ValueError(f"The number of spots per face, {spots_per_face}, is not a perfect square!")
        super().__init__(board.rows)
        self.faces: List[Face] = []
        face_matrix: List[List[Optional[Face]]] = [[None] * 6 for _ in range(6)]
        for r, row in enumerate(range(0, self.dimension * 6, self.dimension)):
            for c, col in enumerate(range(0, self.dimension * 6, self.dimension)):
                face = Face(self, row, col)
                if self.get(row, col) != Space.OUTSIDE:
                    self.faces.append(face)
                    face_matrix[r][c] = face
        if len(self.faces) != 6:
            raise ValueError(f"Found {len(self.faces)} faces but expected 6")
        assert any(f is not None for f in face_matrix[0])
        # now do the folding!
        for r, mrow in enumerate(face_matrix):
            for c, face in enumerate(mrow):
                if face is None:
                    continue
                for facing in Facing:
                    nrow = r + facing.row_delta
                    ncol = c + facing.col_delta
                    if 0 <= nrow < len(face_matrix) and 0 <= ncol < len(face_matrix[nrow]) \
                            and face_matrix[nrow][ncol] is not None:
                        face.add_neighbor(facing, face_matrix[nrow][ncol])

    def face(self, row: int, col: int) -> Face:
        for f in self.faces:
            if f.contains(row, col):
                return f
        raise ValueError(f"<row={row}, col={col}> is not on the cube!")

    @lru_cache(maxsize=10000000)
    def wraps_to(self, row: int, col: int, facing: Facing) -> Tuple[int, int, Facing]:
        return self.face(row, col).wraps_to(row, col, facing)


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
