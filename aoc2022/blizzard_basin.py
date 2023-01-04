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
import heapq
from typing import Dict, List, Iterable, Iterator, Optional, Sequence, Set, Tuple

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


class State:
    __slots__ = "width", "height", "expedition", "_blizzards"

    def __init__(
            self, width: int, height: int, expedition: Position, blizzards: Iterable[Tuple[Direction, Position]],
            _blizzards: Optional[Dict[Position, List[Direction]]] = None
    ):
        self.width: int = width
        self.height: int = height
        self.expedition: Position = expedition
        if _blizzards:
            self._blizzards = _blizzards
        else:
            self._blizzards: Dict[Position, List[Direction]] = {}
            for d, p in blizzards:
                if p not in self._blizzards:
                    self._blizzards[p] = [d]
                else:
                    self._blizzards[p].append(d)

    def __getitem__(self, position: Position) -> Sequence[Direction]:
        if position not in self._blizzards:
            return []
        else:
            return self._blizzards[position]

    def __eq__(self, other):
        return isinstance(other, State) and self.expedition == other.expedition and self._blizzards == other._blizzards

    def __hash__(self):
        return hash((self.expedition, frozenset(self._blizzards.keys())))

    @property
    def goal(self) -> Position:
        return self.height, self.width - 1

    def successors(self) -> Iterator["State"]:
        # first move the blizzards:
        moved_blizzards: List[Tuple[Direction, Position]] = [
            (d, ((row + d.row_delta) % self.height, (col + d.col_delta) % self.width))
            for (row, col), blizzards in self._blizzards.items()
            for d in blizzards
        ]
        base_state = State(width=self.width, height=self.height, expedition=self.expedition, blizzards=moved_blizzards)
        if not base_state[base_state.expedition]:
            # it is safe to wait
            yield base_state
        for d in Direction:
            new_row, new_col = base_state.expedition[0] + d.row_delta, base_state.expedition[1] + d.col_delta
            if (
                    (0 <= new_row < self.height and 0 <= new_col < self.width)
                    and not base_state[(new_row, new_col)]
            ) or ((new_row, new_col) == self.goal):
                # it is a valid move
                yield State(width=self.width, height=self.height, expedition=(new_row, new_col), blizzards=(),
                            _blizzards=base_state._blizzards)

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
            return cls(width=width, height=row - 1, expedition=(-1, 0), blizzards=blizzards)

    def __str__(self):
        rows: List[str] = [
            f"#{['.', 'E'][self.expedition == (-1, 0)]}{'#' * (self.width - 1)}#"
        ]
        for row in range(self.height):
            line: List[str] = ["#"]
            for col in range(self.width):
                p = (row, col)
                if p == self.expedition:
                    line.append("E")
                elif self[p]:
                    blizzards = self[p]
                    if len(blizzards) > 1:
                        line.append(str(len(blizzards)))
                    else:
                        line.append(blizzards[0].symbol)
                else:
                    line.append(".")
            line.append("#")
            rows.append("".join(line))
        rows.append(f"#{'#' * (self.width - 1)}{['.', 'E'][self.expedition == self.goal]}#")
        return "\n".join(rows)


class SearchNode:
    __slots__ = "state", "parent", "path_cost"

    def __init__(self, state: State, parent: Optional["SearchNode"] = None):
        self.state: State = state
        self.parent: Optional[SearchNode] = parent
        if self.parent is None:
            self.path_cost: int = 0
        else:
            self.path_cost = parent.path_cost + 1

    @property
    def f_cost(self):
        return self.path_cost + self.heuristic

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return isinstance(other, SearchNode) and self.state == other.state and self.path_cost == other.path_cost

    def __hash__(self):
        return hash((self.state, self.path_cost))

    @property
    def heuristic(self) -> int:
        goal = self.state.goal
        return abs(goal[0] - self.state.expedition[0]) + abs(goal[1] - self.state.expedition[1])


def search(state: State) -> SearchNode:
    queue = [SearchNode(state)]
    history: Set[SearchNode] = set(queue)
    iteration = 0
    while queue:
        node = heapq.heappop(queue)
        iteration += 1
        if iteration % 1000 == 0:
            print(f"{iteration}\tqueue = {len(queue)}\tdepth = {node.path_cost}\tf-cost = {node.f_cost}")
        if node.state.expedition == node.state.goal:
            # we are done!
            return node
        for successor in node.state.successors():
            succ = SearchNode(successor, parent=node)
            if succ not in history:
                heapq.heappush(queue, succ)
    raise ValueError("Did not find a path to the goal!")


@challenge(day=24)
def fewest_minutes(path: Path) -> int:
    initial_state = State.load(path)
    solution = search(initial_state)
    return solution.path_cost
