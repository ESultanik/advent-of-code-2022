"""
--- Day 24: Blizzard Basin ---
With everything replanted for next year (and with elephants and monkeys to tend the grove), you and the Elves leave for the extraction point.

Partway up the mountain that shields the grove is a flat, open area that serves as the extraction point. It's a bit of a climb, but nothing the expedition can't handle.

At least, that would normally be true; now that the mountain is covered in snow, things have become more difficult than the Elves are used to.

As the expedition reaches a valley that must be traversed to reach the extraction site, you find that strong, turbulent winds are pushing small blizzards of snow and sharp ice around the valley. It's a good thing everyone packed warm clothes! To make it across safely, you'll need to find a way to avoid them.

Fortunately, it's easy to see all of this from the entrance to the valley, so you make a map of the valley and the blizzards (your puzzle input). For example:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
The walls of the valley are drawn as #; everything else is ground. Clear ground - where there is currently no blizzard - is drawn as .. Otherwise, blizzards are drawn with an arrow indicating their direction of motion: up (^), down (v), left (<), or right (>).

The above map includes two blizzards, one moving right (>) and one moving down (v). In one minute, each blizzard moves one position in the direction it is pointing:

#.#####
#.....#
#.>...#
#.....#
#.....#
#...v.#
#####.#
Due to conservation of blizzard energy, as a blizzard reaches the wall of the valley, a new blizzard forms on the opposite side of the valley moving in the same direction. After another minute, the bottom downward-moving blizzard has been replaced with a new downward-moving blizzard at the top of the valley instead:

#.#####
#...v.#
#..>..#
#.....#
#.....#
#.....#
#####.#
Because blizzards are made of tiny snowflakes, they pass right through each other. After another minute, both blizzards temporarily occupy the same position, marked 2:

#.#####
#.....#
#...2.#
#.....#
#.....#
#.....#
#####.#
After another minute, the situation resolves itself, giving each blizzard back its personal space:

#.#####
#.....#
#....>#
#...v.#
#.....#
#.....#
#####.#
Finally, after yet another minute, the rightward-facing blizzard on the right is replaced with a new one on the left facing the same direction:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
This process repeats at least as long as you are observing it, but probably forever.

Here is a more complex example:

#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
Your expedition begins in the only non-wall position in the top row and needs to reach the only non-wall position in the bottom row. On each minute, you can move up, down, left, or right, or you can wait in place. You and the blizzards act simultaneously, and you cannot share a position with a blizzard.

In the above example, the fastest way to reach your goal requires 18 steps. Drawing the position of the expedition as E, one way to achieve this is:

Initial state:
#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#

Minute 1, move down:
#.######
#E>3.<.#
#<..<<.#
#>2.22.#
#>v..^<#
######.#

Minute 2, move down:
#.######
#.2>2..#
#E^22^<#
#.>2.^>#
#.>..<.#
######.#

Minute 3, wait:
#.######
#<^<22.#
#E2<.2.#
#><2>..#
#..><..#
######.#

Minute 4, move up:
#.######
#E<..22#
#<<.<..#
#<2.>>.#
#.^22^.#
######.#

Minute 5, move right:
#.######
#2Ev.<>#
#<.<..<#
#.^>^22#
#.2..2.#
######.#

Minute 6, move right:
#.######
#>2E<.<#
#.2v^2<#
#>..>2>#
#<....>#
######.#

Minute 7, move down:
#.######
#.22^2.#
#<vE<2.#
#>>v<>.#
#>....<#
######.#

Minute 8, move left:
#.######
#.<>2^.#
#.E<<.<#
#.22..>#
#.2v^2.#
######.#

Minute 9, move up:
#.######
#<E2>>.#
#.<<.<.#
#>2>2^.#
#.v><^.#
######.#

Minute 10, move right:
#.######
#.2E.>2#
#<2v2^.#
#<>.>2.#
#..<>..#
######.#

Minute 11, wait:
#.######
#2^E^2>#
#<v<.^<#
#..2.>2#
#.<..>.#
######.#

Minute 12, move down:
#.######
#>>.<^<#
#.<E.<<#
#>v.><>#
#<^v^^>#
######.#

Minute 13, move down:
#.######
#.>3.<.#
#<..<<.#
#>2E22.#
#>v..^<#
######.#

Minute 14, move right:
#.######
#.2>2..#
#.^22^<#
#.>2E^>#
#.>..<.#
######.#

Minute 15, move right:
#.######
#<^<22.#
#.2<.2.#
#><2>E.#
#..><..#
######.#

Minute 16, move right:
#.######
#.<..22#
#<<.<..#
#<2.>>E#
#.^22^.#
######.#

Minute 17, move down:
#.######
#2.v.<>#
#<.<..<#
#.^>^22#
#.2..2E#
######.#

Minute 18, move down:
#.######
#>2.<.<#
#.2v^2<#
#>..>2>#
#<....>#
######E#
What is the fewest number of minutes required to avoid the blizzards and reach the goal?
"""

from enum import Enum
from functools import lru_cache
import heapq
from math import lcm
from typing import List, Iterator, Optional, Set, Tuple

from . import challenge, Path


class Direction(Enum):
    UP = ("^", -1, 0)
    DOWN = ("v", 1, 0)
    RIGHT = (">", 0, 1)
    LEFT = ("<", 0, -1)

    def __init__(self, symbol: str, row_delta: int, col_delta: int):
        self.symbol: str = symbol
        self.row_delta: int = row_delta
        self.col_delta: int = col_delta


Position = Tuple[int, int]


class Blizzards:
    def __init__(self, height: int, width: int, blizzards: Tuple[Tuple[Direction, Position], ...]):
        self.height: int = height
        self.width: int = width
        self.initial_state: Tuple[Tuple[Direction, Position], ...] = blizzards
        self.max_state: int = lcm(height, width)
        self.blizzards: List[Optional[List[List[int]]]] = [None] * self.max_state

    @lru_cache(maxsize=100000)
    def blizzard_positions(self, state: int) -> Tuple[Position, ...]:
        return tuple((
            (
                (row + direction.row_delta * state) % self.height,
                (col + direction.col_delta * state) % self.width
            )
            for direction, (row, col) in self.initial_state
        ))

    def is_open(self, state: int, position: Position) -> bool:
        if position[0] < 0 or position[0] >= self.height or position[1] < 0 or position[1] >= self.width:
            return True
        state %= self.max_state
        if self.blizzards[state] is None:
            self.blizzards[state] = [[0] * self.width for _ in range(self.height)]
            for direction, (row, col) in self.initial_state:
                new_row = (row + direction.row_delta * state) % self.height
                new_col = (col + direction.col_delta * state) % self.width
                self.blizzards[state][new_row][new_col] += 1
        return self.blizzards[state][position[0]][position[1]] == 0


class State:
    __slots__ = "width", "height", "expedition", "blizzards", "blizzard_state", "goal"

    def __init__(self, expedition: Position, blizzards: Blizzards, blizzard_state: int = 0,
                 goal: Optional[Position] = None):
        self.expedition: Position = expedition
        self.blizzards: Blizzards = blizzards
        self.blizzard_state = blizzard_state % blizzards.max_state
        if goal is None:
            self.goal: Position = (self.blizzards.height, self.blizzards.width - 1)
        else:
            self.goal = goal

    def is_open(self, position: Position) -> bool:
        return self.blizzards.is_open(self.blizzard_state, position)

    def all_blizzards(self) -> Iterator[Tuple[Direction, Position]]:
        for direction, (row, col) in self.blizzards.initial_state:
            blizzard_pos = (
                (row + direction.row_delta * self.blizzard_state) % self.blizzards.height,
                (col + direction.col_delta * self.blizzard_state) % self.blizzards.width
            )
            yield direction, blizzard_pos

    def blizzards_at(self, position: Position) -> Iterator[Direction]:
        for direction, (row, col) in self.blizzards.initial_state:
            blizzard_pos = (
                (row + direction.row_delta * self.blizzard_state) % self.blizzards.height,
                (col + direction.col_delta * self.blizzard_state) % self.blizzards.width
            )
            if position == blizzard_pos:
                yield direction

    def __eq__(self, other):
        return self.expedition == other.expedition and self.blizzard_state == other.initial_state

    def __hash__(self):
        return hash((self.expedition, self.blizzard_state))

    def next_state(self) -> "State":
        """This does not check if the expedition gets caught in a blizzard"""
        return State(
            expedition=self.expedition,
            blizzards=self.blizzards,
            blizzard_state=self.blizzard_state + 1,
            goal=self.goal
        )

    def successors(self) -> Iterator["State"]:
        # first move the blizzards:
        base_state = self.next_state()
        if base_state.is_open(base_state.expedition):
            # it is safe to wait
            yield base_state
        for d in Direction:
            new_pos = base_state.expedition[0] + d.row_delta, base_state.expedition[1] + d.col_delta
            if (
                    (0 <= new_pos[0] < self.blizzards.height and 0 <= new_pos[1] < self.blizzards.width)
                    and base_state.is_open(new_pos)
            ) or (new_pos == self.goal):
                # it is a valid move
                yield State(
                    expedition=new_pos,
                    blizzards=base_state.blizzards,
                    blizzard_state=base_state.blizzard_state,
                    goal=self.goal
                )

    @classmethod
    def load(cls, path: Path) -> "State":
        width = 0
        blizzards: List[Tuple[Direction, Position]] = []
        with open(path, "r") as f:
            for row, line in enumerate(f):
                line = line.strip()[1:-1]
                if row == 0:
                    width = len(line)
                    assert line.find(".") == 0
                    continue
                for col, c in enumerate(line):
                    for d in Direction:
                        if c == d.symbol:
                            blizzards.append((d, (row - 1, col)))
                            break
            return cls(expedition=(-1, 0), blizzards=Blizzards(width=width, height=row - 1, blizzards=tuple(blizzards)))

    def __str__(self):
        board: List[List[str]] = [list("." * self.blizzards.width) for _ in range(self.blizzards.height)]
        for direction, (row, col) in self.all_blizzards():
            if board[row][col] == ".":
                board[row][col] = direction.symbol
            elif any(board[row][col] == d.symbol for d in Direction):
                board[row][col] = "2"
            else:
                board[row][col] = chr(ord(board[row][col]) + 1)
        er, ec = self.expedition
        if 0 <= er < len(board) and 0 <= ec < len(board[er]):
            board[er][ec] = "E"
        rows = [f"#{['.', 'E'][self.expedition == (-1, 0)]}{'#' * (self.blizzards.width - 1)}#"] + [
            f"#{''.join(row)}#"
            for row in board
        ] + [f"#{'#' * (self.blizzards.width - 1)}{['.', 'E'][self.expedition == self.goal]}#"]
        return "\n".join(rows)


def calculate_fewest_minutes(state: State) -> int:
    possible_positions: Set[Position] = {state.expedition}
    rounds = 0
    while possible_positions:
        state = state.next_state()
        rounds += 1
        next_possible_positions: Set[Position] = set()
        if rounds % 30 == 0:
            closest = min(abs(state.goal[0] - p[0]) + abs(state.goal[1] - p[1]) for p in possible_positions)
            print(rounds, len(possible_positions), closest)
        for pos in possible_positions:
            state.expedition = pos
            # print(str(state))
            if state.is_open(pos):
                # it is safe to wait
                next_possible_positions.add(pos)
            for d in Direction:
                new_pos = state.expedition[0] + d.row_delta, state.expedition[1] + d.col_delta
                if new_pos == state.goal:
                    return rounds
                elif (
                        (0 <= new_pos[0] < state.blizzards.height and 0 <= new_pos[1] < state.blizzards.width)
                        and state.is_open(new_pos)
                ):
                    # it is a valid move
                    next_possible_positions.add(new_pos)
        possible_positions = next_possible_positions
    raise ValueError("No solution!")


@challenge(day=24)
def fewest_minutes(path: Path) -> int:
    state = State.load(path)
    return calculate_fewest_minutes(state)


@challenge(day=24)
def back_and_forth(path: Path) -> int:
    state = State.load(path)
    time_to_goal = calculate_fewest_minutes(state)
    print(f"Initial time to the goal: {time_to_goal}")
    # set the goal to be the start
    state.expedition = state.goal
    state.goal = (-1, 0)
    state.blizzard_state = time_to_goal
    time_back_to_start = calculate_fewest_minutes(state)
    print(f"Time to get back to the start: {time_back_to_start}")
    # now go back to the goal again
    state.blizzard_state = time_to_goal + time_back_to_start
    state.expedition = state.goal
    state.goal = (state.blizzards.height, state.blizzards.width - 1)
    time_to_goal_again = calculate_fewest_minutes(state)
    print(f"Time to get back to the goal again: {time_to_goal_again}")
    return time_to_goal + time_back_to_start + time_to_goal_again
