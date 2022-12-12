"""
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
"""

from enum import Enum
import heapq
from typing import Iterator, List, Optional, Set, Tuple

from . import challenge, Path


class Move(Enum):
    UP = "^"
    LEFT = "<"
    DOWN = "v"
    RIGHT = ">"


class State:
    def __init__(self, height_map: List[str], row: Optional[int] = None, col: Optional[int] = None):
        self.height_map: List[str] = height_map
        if row is None or col is None:
            for i, r in enumerate(height_map):
                found = False
                for j, c in enumerate(r):
                    if c == "S":
                        self.row: int = i
                        self.col: int = j
                        found = True
                        break
                if found:
                    break
            else:
                raise ValueError(f"No start position in height map!")
        else:
            self.row = row
            self.col = col

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return isinstance(other, State) and other.row == self.row and other.col == self.col

    @property
    def elevation(self) -> int:
        c = self.height_map[self.row][self.col]
        if c == "S":
            c = "a"
        elif c == "E":
            c = "z"
        return ord(c) - ord("a")

    def successors(self) -> Iterator[Tuple[Move, "State"]]:
        for move in Move:
            try:
                yield move, self.apply(move)
            except ValueError:
                pass

    def apply(self, move: Move) -> "State":
        to_row = self.row
        to_col = self.col
        match move:
            case Move.UP:
                to_row -= 1
            case Move.DOWN:
                to_row += 1
            case Move.RIGHT:
                to_col += 1
            case Move.LEFT:
                to_col -= 1
        if to_row < 0 or to_row >= len(self.height_map) or to_col < 0 or to_col >= len(self.height_map[to_row]):
            raise ValueError(f"Invalid end position for {move!r}: (row={to_row}, col={to_col})")
        start_elevation = self.elevation
        next_state = State(self.height_map, to_row, to_col)
        next_elevation = next_state.elevation
        if next_elevation > start_elevation + 1:
            raise ValueError(f"Move {move!r} is up too high an elevation: {start_elevation} -> {next_elevation}")
        return next_state


class SearchNode:
    def __init__(self, state: State, parent: Optional["SearchNode"] = None, previous_move: Optional[Move] = None):
        self.state: State = state
        if parent is None:
            self.parent: Optional[SearchNode] = None
            self.previous_move: Optional[Move] = None
            self.path_cost: int = 0
            for i, r in enumerate(state.height_map):
                found = False
                for j, c in enumerate(r):
                    if c == "E":
                        self.goal: Tuple[int, int] = (i, j)
                        found = True
                        break
                if found:
                    break
            else:
                raise ValueError(f"No goal position in height map!")
        else:
            self.previous_move = previous_move
            self.parent = parent
            self.goal = parent.goal
            self.path_cost = parent.path_cost + 1
        self.heuristic = abs(self.state.row - self.goal[0]) + abs(self.state.col - self.goal[1])

    @property
    def is_goal(self) -> bool:
        return self.state.row == self.goal[0] and self.state.col == self.goal[1]

    @property
    def f_cost(self) -> int:
        return self.path_cost + self.heuristic

    def __lt__(self, other):
        return isinstance(other, SearchNode) and self.f_cost < other.f_cost

    def __eq__(self, other):
        return isinstance(other, SearchNode) and self.state == other.state and self.path_cost == other.path_cost

    def __hash__(self):
        return hash((self.state, self.path_cost))


def solve(*states: State) -> Iterator[SearchNode]:
    queue: List[SearchNode] = []
    for state in states:
        heapq.heappush(queue, SearchNode(state))
    solution: Optional[SearchNode] = None
    history: Set[SearchNode] = set(queue)
    i = 0
    while queue:
        i += 1
        node = heapq.heappop(queue)
        if i % 10000 == 0:
            print(f"Iteration: {i}\tQueue: {len(queue)}\tBest so far: {node.f_cost}")
        if node.is_goal:
            solution = node
            break
        for move, successor in node.state.successors():
            next_node = SearchNode(successor, parent=node, previous_move=move)
            if next_node not in history:
                history.add(next_node)
                heapq.heappush(queue, next_node)
    if solution is None:
        raise ValueError("No solution!")
    states: List[SearchNode] = []
    while solution is not None:
        states.append(solution)
        solution = solution.parent
    return reversed(states)


def parse(path: Path) -> List[str]:
    height_map: List[str] = []
    with open(path, "r") as f:
        for line in f:
            height_map.append(line.strip())
    return height_map


@challenge(day=12)
def fewest_steps_to_best_signal(path: Path) -> int:
    height_map = parse(path)
    return sum(1 for _ in solve(State(height_map))) - 1


@challenge(day=12)
def multi_source_shortest_path(path: Path) -> int:
    height_map = parse(path)
    low_states: List[State] = []
    for i, row in enumerate(height_map):
        for j, c in enumerate(row):
            if c == "S" or c == "a":
                low_states.append(State(height_map=height_map, row=i, col=j))
    return sum(1 for _ in solve(*low_states)) - 1
