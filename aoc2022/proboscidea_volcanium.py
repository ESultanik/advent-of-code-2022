"""
--- Day 16: Proboscidea Volcanium ---
The sensors have led you to the origin of the distress signal: yet another handheld device, just like the one the Elves gave you. However, you don't see any Elves around; instead, the device is surrounded by elephants! They must have gotten lost in these tunnels, and one of the elephants apparently figured out how to turn on the distress signal.

The ground rumbles again, much stronger this time. What kind of cave is this, exactly? You scan the cave with your handheld device; it reports mostly igneous rock, some ash, pockets of pressurized gas, magma... this isn't just a cave, it's a volcano!

You need to get the elephants out of here, quickly. Your device estimates that you have 30 minutes before the volcano erupts, so you don't have time to go back out the way you came in.

You scan the cave for other options and discover a network of pipes and pressure-release valves. You aren't sure how such a system got into a volcano, but you don't have time to complain; your device produces a report (your puzzle input) of each valve's flow rate if it were opened (in pressure per minute) and the tunnels you could use to move between the valves.

There's even a valve in the room you and the elephants are currently standing in labeled AA. You estimate it will take you one minute to open a single valve and one minute to follow any tunnel from one valve to another. What is the most pressure you could release?

For example, suppose you had the following scan output:

Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
All of the valves begin closed. You start at valve AA, but it must be damaged or jammed or something: its flow rate is 0, so there's no point in opening it. However, you could spend one minute moving to valve BB and another minute opening it; doing so would release pressure during the remaining 28 minutes at a flow rate of 13, a total eventual pressure release of 28 * 13 = 364. Then, you could spend your third minute moving to valve CC and your fourth minute opening it, providing an additional 26 minutes of eventual pressure release at a flow rate of 2, or 52 total pressure released by valve CC.

Making your way through the tunnels like this, you could probably open many or all of the valves by the time 30 minutes have elapsed. However, you need to release as much pressure as possible, so you'll need to be methodical. Instead, consider this approach:

== Minute 1 ==
No valves are open.
You move to valve DD.

== Minute 2 ==
No valves are open.
You open valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You move to valve CC.

== Minute 4 ==
Valve DD is open, releasing 20 pressure.
You move to valve BB.

== Minute 5 ==
Valve DD is open, releasing 20 pressure.
You open valve BB.

== Minute 6 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve AA.

== Minute 7 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve II.

== Minute 8 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve JJ.

== Minute 9 ==
Valves BB and DD are open, releasing 33 pressure.
You open valve JJ.

== Minute 10 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve II.

== Minute 11 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve AA.

== Minute 12 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve DD.

== Minute 13 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve EE.

== Minute 14 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve FF.

== Minute 15 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve GG.

== Minute 16 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve HH.

== Minute 17 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You open valve HH.

== Minute 18 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve GG.

== Minute 19 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve FF.

== Minute 20 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve EE.

== Minute 21 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve EE.

== Minute 22 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve DD.

== Minute 23 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve CC.

== Minute 24 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You open valve CC.

== Minute 25 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 27 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 28 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 29 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 30 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
This approach lets you release the most pressure possible in 30 minutes with this valve layout, 1651.

Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import heapq
import re
from typing import Dict, FrozenSet, Iterator, List, Optional

from . import challenge, Path


VALVE_PATTERN: re.Pattern = re.compile(r"Valve (\S+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")


class Valve:
    def __init__(self, name: str, flow_rate: int):
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.neighbors: Dict[str, Valve] = {}

    def dfs(self) -> Iterator["Valve"]:
        stack = [self]
        history = set(stack)
        while stack:
            valve = stack.pop()
            yield valve
            neighbors = set(valve.neighbors.values()) - history
            history |= neighbors
            stack.extend(neighbors)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Valve) and self.name == other.name

    def __str__(self):
        return f"Valve {self.name} has flow rate={self.flow_rate}; tunnels lead to valves " \
               f"{', '.join(sorted(self.neighbors.keys()))}"


def load(path: Path) -> Dict[str, Valve]:
    valves: Dict[str, Valve] = {}
    neighbors: Dict[Valve, List[str]] = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            m = VALVE_PATTERN.match(line)
            if not m:
                raise ValueError(repr(line))
            name = m.group(1)
            if name in valves:
                raise ValueError(f"Duplicate valve: {name}")
            valve = Valve(name=name, flow_rate=int(m.group(2)))
            valves[valve.name] = valve
            neighbors[valve] = [n.strip() for n in m.group(3).split(",")]
    for valve, neighbor_names in neighbors.items():
        valve.neighbors = {
            name: valves[name]
            for name in neighbor_names
        }
    return valves


@dataclass(frozen=True, slots=True)
class State:
    location: Valve
    open_valves: FrozenSet[Valve]
    elephant_location: Optional[Valve] = None

    @property
    def released_pressure(self):
        return sum(v.flow_rate for v in self.open_valves)

    def __str__(self):
        return f"Valves {', '.join(v.name for v in sorted(self.open_valves, key=lambda p: p.name))} " \
               f"are open, releasing {self.released_pressure} pressure."


class Move(ABC):
    __slots__ = "valve",

    def __init__(self, valve: Valve):
        self.valve: Valve = valve

    @abstractmethod
    def apply(self, state: State) -> State:
        raise NotImplementedError()


class MoveTo(Move):
    def apply(self, state: State) -> State:
        if state.location.name not in self.valve.neighbors:
            raise ValueError(f"{self.valve.name} is not connected to {state.location.name}; "
                             f"its neighbors are {', '.join(self.valve.neighbors.keys())}")
        return State(
            location=self.valve,
            open_valves=state.open_valves
        )


class OpenValve(Move):
    def apply(self, state: State) -> State:
        if state.location != self.valve:
            raise ValueError(f"Not at location {state.location}!")
        return State(
            location=state.location,
            open_valves=state.open_valves | frozenset({self.valve})
        )


class ElephantMoveTo(Move):
    def apply(self, state: State) -> State:
        if state.elephant_location is None:
            raise ValueError("No elephant!")
        elif state.elephant_location.name not in self.valve.neighbors:
            raise ValueError(f"{self.valve.name} is not connected to {state.location.name}; "
                             f"its neighbors are {', '.join(self.valve.neighbors.keys())}")
        return State(
            location=state.location,
            elephant_location=state.elephant_location,
            open_valves=state.open_valves
        )


class SearchNode:
    __slots__ = "state", "parent", "total_released", "release_potential", "all_valves", "remaining_minutes"

    def __init__(self, state: State, parent: Optional["SearchNode"] = None, remaining_minutes: int = 29):
        self.state: State = state
        if parent is None:
            self.remaining_minutes: int = remaining_minutes
            self.total_released: int = 0
            self.parent: Optional[SearchNode] = None
            self.all_valves: List[Valve] = sorted(state.location.dfs(), reverse=True, key=lambda v: v.flow_rate)
        else:
            self.remaining_minutes = parent.remaining_minutes - 1
            if self.remaining_minutes < 0:
                raise ValueError("No time left!")
            self.total_released = parent.total_released + state.released_pressure
            self.parent = parent
            self.all_valves = parent.all_valves
        remaining_minutes = self.remaining_minutes + 1
        remaining_openings = remaining_minutes // 2
        if remaining_minutes % 2 != 0 and self.state.location not in self.state.open_valves:
            # we can also open the local valve
            remaining_openings += 1
        remaining_valves = [v for v in self.all_valves if v not in self.state.open_valves]
        self.release_potential: int = self.total_released + sum(
            v.flow_rate * remaining_minutes for v in self.state.open_valves
        ) + sum(
            v.flow_rate * (remaining_minutes - i)
            for i, v in enumerate(remaining_valves[:remaining_openings])
        )

    @property
    def minute(self) -> int:
        m = 1
        s = self
        while s.parent is not None:
            m += 1
            s = s.parent
        return m

    def successors(self) -> Iterator["SearchNode"]:
        if self.remaining_minutes <= 0:
            return
        if self.state.location not in self.state.open_valves and self.state.location.flow_rate > 0:
            yield SearchNode(OpenValve(self.state.location).apply(self.state), self)
        for neighbor in self.state.location.neighbors.values():
            yield SearchNode(MoveTo(neighbor).apply(self.state), self)
        if len(self.state.open_valves) == len(self.all_valves):
            # all of the valves are open, so do nothing:
            yield SearchNode(self.state, self)

    def __lt__(self, other):
        return isinstance(other, SearchNode) and self.release_potential > other.release_potential

    def __eq__(self, other):
        return isinstance(other, SearchNode) and other.state == self.state and \
               other.remaining_minutes == self.remaining_minutes and self.total_released == other.total_released

    def __hash__(self):
        return hash((self.state, self.remaining_minutes, self.total_released))

    def __str__(self):
        if self.parent is not None:
            s = f"{self.parent!s}"
            if self.parent.state.location != self.state.location:
                s = f"{s}You move to valve {self.state.location.name}\n\n"
            elif self.parent.state.open_valves != self.state.open_valves:
                opened = self.state.open_valves - self.parent.state.open_valves
                assert len(opened) == 1
                s = f"{s}You open valve {next(iter(opened)).name}\n\n"
            else:
                s = f"{s}\n"
        else:
            s = ""
        s = f"{s}== Minute {self.minute} ==\n"
        if self.state.open_valves:
            s = f"{s}Valves {', '.join((v.name for v in self.state.open_valves))} are open, " \
                f"releasing {self.state.released_pressure} pressure.\n"
        else:
            s = f"{s}No valves are open.\n"
        return s


@challenge(day=16)
def max_pressure(path: Path) -> int:
    valves = load(path)
    for valve_name in sorted(valves.keys()):
        print(str(valves[valve_name]))
    initial_state = State(location=valves["AA"], open_valves=frozenset())
    queue = [SearchNode(initial_state)]
    history = set()
    i = 0
    while queue:
        node = heapq.heappop(queue)
        i += 1
        if i % 10000 == 0:
            print(node.release_potential)
        if node.remaining_minutes == 0:
            print(node)
            return node.total_released
        successors = {s for s in node.successors() if s not in history}
        for successor in successors:
            heapq.heappush(queue, successor)
        history |= successors
    else:
        raise ValueError("No solution!")


"""
--- Part Two ---
You're worried that even with an optimal approach, the pressure released won't be enough. What if you got one of the elephants to help you?

It would take you 4 minutes to teach an elephant how to open the right valves in the right order, leaving you with only 26 minutes to actually execute your plan. Would having two of you working together be better, even if it means having less time? (Assume that you teach the elephant before opening any valves yourself, giving you both the same full 26 minutes.)

In the example above, you could teach the elephant to help you as follows:

== Minute 1 ==
No valves are open.
You move to valve II.
The elephant moves to valve DD.

== Minute 2 ==
No valves are open.
You move to valve JJ.
The elephant opens valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You open valve JJ.
The elephant moves to valve EE.

== Minute 4 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve II.
The elephant moves to valve FF.

== Minute 5 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve AA.
The elephant moves to valve GG.

== Minute 6 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve BB.
The elephant moves to valve HH.

== Minute 7 ==
Valves DD and JJ are open, releasing 41 pressure.
You open valve BB.
The elephant opens valve HH.

== Minute 8 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve CC.
The elephant moves to valve GG.

== Minute 9 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve CC.
The elephant moves to valve FF.

== Minute 10 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant moves to valve EE.

== Minute 11 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant opens valve EE.

(At this point, all valves are open.)

== Minute 12 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 20 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
With the elephant helping, after 26 minutes, the best you could do would release a total of 1707 pressure.

With you and an elephant working together for 26 minutes, what is the most pressure you could release?
"""

