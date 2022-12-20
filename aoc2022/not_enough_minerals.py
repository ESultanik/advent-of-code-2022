"""
--- Day 19: Not Enough Minerals ---
Your scans show that the lava did indeed form obsidian!

The wind has changed direction enough to stop sending lava droplets toward you, so you and the elephants exit the cave. As you do, you notice a collection of geodes around the pond. Perhaps you could use the obsidian to create some geode-cracking robots and break them open?

To collect the obsidian from the bottom of the pond, you'll need waterproof obsidian-collecting robots. Fortunately, there is an abundant amount of clay nearby that you can use to make them waterproof.

In order to harvest the clay, you'll need special-purpose clay-collecting robots. To make any type of robot, you'll need ore, which is also plentiful but in the opposite direction from the clay.

Collecting ore requires ore-collecting robots with big drills. Fortunately, you have exactly one ore-collecting robot in your pack that you can use to kickstart the whole operation.

Each robot can collect 1 of its resource type per minute. It also takes one minute for the robot factory (also conveniently from your pack) to construct any type of robot, although it consumes the necessary resources available when construction begins.

The robot factory has many blueprints (your puzzle input) you can choose from, but once you've configured it with a blueprint, you can't change it. You'll need to work out which blueprint is best.

For example:

Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
(Blueprints have been line-wrapped here for legibility. The robot factory's actual assortment of blueprints are provided one blueprint per line.)

The elephants are starting to look hungry, so you shouldn't take too long; you need to figure out which blueprint would maximize the number of opened geodes after 24 minutes by figuring out which robots to build and when to build them.

Using blueprint 1 in the example above, the largest number of geodes you could open in 24 minutes is 9. One way to achieve that is:

== Minute 1 ==
1 ore-collecting robot collects 1 ore; you now have 1 ore.

== Minute 2 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.

== Minute 3 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
The new clay-collecting robot is ready; you now have 1 of them.

== Minute 4 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
1 clay-collecting robot collects 1 clay; you now have 1 clay.

== Minute 5 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
1 clay-collecting robot collects 1 clay; you now have 2 clay.
The new clay-collecting robot is ready; you now have 2 of them.

== Minute 6 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
2 clay-collecting robots collect 2 clay; you now have 4 clay.

== Minute 7 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
2 clay-collecting robots collect 2 clay; you now have 6 clay.
The new clay-collecting robot is ready; you now have 3 of them.

== Minute 8 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
3 clay-collecting robots collect 3 clay; you now have 9 clay.

== Minute 9 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
3 clay-collecting robots collect 3 clay; you now have 12 clay.

== Minute 10 ==
1 ore-collecting robot collects 1 ore; you now have 4 ore.
3 clay-collecting robots collect 3 clay; you now have 15 clay.

== Minute 11 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 2 ore.
3 clay-collecting robots collect 3 clay; you now have 4 clay.
The new obsidian-collecting robot is ready; you now have 1 of them.

== Minute 12 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
3 clay-collecting robots collect 3 clay; you now have 7 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 1 obsidian.
The new clay-collecting robot is ready; you now have 4 of them.

== Minute 13 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
4 clay-collecting robots collect 4 clay; you now have 11 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 2 obsidian.

== Minute 14 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 15 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 3 obsidian.

== Minute 15 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
4 clay-collecting robots collect 4 clay; you now have 5 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 4 obsidian.
The new obsidian-collecting robot is ready; you now have 2 of them.

== Minute 16 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
4 clay-collecting robots collect 4 clay; you now have 9 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.

== Minute 17 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 13 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.

== Minute 18 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
1 ore-collecting robot collects 1 ore; you now have 2 ore.
4 clay-collecting robots collect 4 clay; you now have 17 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 3 obsidian.
The new geode-cracking robot is ready; you now have 1 of them.

== Minute 19 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 21 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 5 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 1 open geode.

== Minute 20 ==
1 ore-collecting robot collects 1 ore; you now have 4 ore.
4 clay-collecting robots collect 4 clay; you now have 25 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 7 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 2 open geodes.

== Minute 21 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 29 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 2 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 3 open geodes.
The new geode-cracking robot is ready; you now have 2 of them.

== Minute 22 ==
1 ore-collecting robot collects 1 ore; you now have 4 ore.
4 clay-collecting robots collect 4 clay; you now have 33 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 4 obsidian.
2 geode-cracking robots crack 2 geodes; you now have 5 open geodes.

== Minute 23 ==
1 ore-collecting robot collects 1 ore; you now have 5 ore.
4 clay-collecting robots collect 4 clay; you now have 37 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.
2 geode-cracking robots crack 2 geodes; you now have 7 open geodes.

== Minute 24 ==
1 ore-collecting robot collects 1 ore; you now have 6 ore.
4 clay-collecting robots collect 4 clay; you now have 41 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.
2 geode-cracking robots crack 2 geodes; you now have 9 open geodes.
However, by using blueprint 2 in the example above, you could do even better: the largest number of geodes you could open in 24 minutes is 12.

Determine the quality level of each blueprint by multiplying that blueprint's ID number with the largest number of geodes that can be opened in 24 minutes using that blueprint. In this example, the first blueprint has ID 1 and can open 9 geodes, so its quality level is 9. The second blueprint has ID 2 and can open 12 geodes, so its quality level is 24. Finally, if you add up the quality levels of all of the blueprints in the list, you get 33.

Determine the quality level of each blueprint using the largest number of geodes it could produce in 24 minutes. What do you get if you add up the quality level of all of the blueprints in your list?
"""

from dataclasses import dataclass
import heapq
import re
from typing import Iterator, List, Set

from tqdm import tqdm

from . import challenge, Path

BLUEPRINT_PATTERN: re.Pattern = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs "
    r"(\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
)


@dataclass(frozen=True, slots=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0

    def __hash__(self):
        return hash((self.ore, self.clay, self.obsidian, self.geodes))

    def __eq__(self, other):
        return isinstance(other, Resources) and self.ore == other.ore and self.clay == other.clay \
            and self.obsidian == other.obsidian and self.geodes == other.geodes

    def __lt__(self, other):
        return isinstance(other, Resources) and self.ore < other.ore and self.clay < other.clay \
            and self.obsidian < other.obsidian and self.geodes < other.geodes

    def __le__(self, other):
        return isinstance(other, Resources) and self.ore <= other.ore and self.clay <= other.clay \
            and self.obsidian <= other.obsidian and self.geodes <= other.geodes

    def is_better_than(self, other: "Resources") -> bool:
        return self.geodes > other.geodes or (
                self.geodes == other.geodes and (self.obsidian > other.obsidian or (
                    self.obsidian == other.obsidian and (self.clay > other.clay or (
                        self.clay == other.clay and self.ore > other.ore
                    ))
                ))
        )

    def __add__(self, addend: "Resources") -> "Resources":
        return Resources(
            ore=self.ore + addend.ore,
            clay=self.clay + addend.clay,
            obsidian=self.obsidian + addend.obsidian,
            geodes=self.geodes + addend.geodes
        )

    def __sub__(self, subtrahend: "Resources") -> "Resources":
        return Resources(
            ore=self.ore - subtrahend.ore,
            clay=self.clay - subtrahend.clay,
            obsidian=self.obsidian - subtrahend.obsidian,
            geodes=self.geodes - subtrahend.geodes
        )

    def __mul__(self, factor: int) -> "Resources":
        return Resources(
            ore=self.ore * factor,
            clay=self.clay * factor,
            obsidian=self.obsidian * factor,
            geodes=self.geodes * factor
        )


@dataclass(frozen=True, slots=True, unsafe_hash=True, eq=True)
class MiningState:
    minute: int = 0
    resources: Resources = Resources()
    ore_bots: int = 1
    clay_bots: int = 0
    obsidian_bots: int = 0
    geode_bots: int = 0

    def resources_upper_bound(self, at_time: int) -> Resources:
        remaining_minutes = max(0, at_time - self.minute)
        if remaining_minutes <= 0:
            return self.resources
        # assume we build one geode bot every minute for the remaining time
        # new_geodes = sum(self.geode_bots + i for i in range(remaining_minutes))
        new_resources = Resources(
            ore=(remaining_minutes * (2 * self.ore_bots + remaining_minutes - 1)) // 2,
            clay=(remaining_minutes * (2 * self.clay_bots + remaining_minutes - 1)) // 2,
            obsidian=(remaining_minutes * (2 * self.obsidian_bots + remaining_minutes - 1)) // 2,
            geodes=(remaining_minutes * (2 * self.geode_bots + remaining_minutes - 1)) // 2
        )
        return self.resources + new_resources

    def geodes_lower_bound(self, at_time: int) -> int:
        return self.resources.geodes + max(0, at_time - self.minute) * self.geode_bots

    def __lt__(self, other):
        return self.resources.is_better_than(other.resources)


class SearchNode:
    __slots__ = "state", "geodes_upper_bound"

    def __init__(self, state: MiningState, geodes_upper_bound: int):
        self.state: MiningState = state
        self.geodes_upper_bound: int = geodes_upper_bound

    @classmethod
    def make(cls, state: MiningState, minutes: int) -> "SearchNode":
        resources_upper_bound = state.resources_upper_bound(minutes)
        assert resources_upper_bound.geodes >= state.resources.geodes
        return SearchNode(state, resources_upper_bound.geodes)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return isinstance(other, SearchNode) and other.state == self.state

    def __lt__(self, other):
        return isinstance(other, SearchNode) and (
                self.geodes_upper_bound > other.geodes_upper_bound #or
                #(self.geodes_upper_bound == other.geodes_upper_bound
                # and self.state.resources.is_better_than(other.state.resources))
        )


class Blueprint:
    def __init__(
            self,
            id_number: int,
            ore_cost: Resources,
            clay_cost: Resources,
            obsidian_cost: Resources,
            geode_cost: Resources
    ):
        self.id_number: int = id_number
        self.ore_cost: Resources = ore_cost
        self.clay_cost: Resources = clay_cost
        self.obsidian_cost: Resources = obsidian_cost
        self.geode_cost: Resources = geode_cost

    @classmethod
    def parse(cls, line: str) -> "Blueprint":
        m = BLUEPRINT_PATTERN.match(line.strip())
        if not m:
            raise ValueError(line)
        return cls(
            id_number=int(m.group(1)),
            ore_cost=Resources(ore=int(m.group(2))),
            clay_cost=Resources(ore=int(m.group(3))),
            obsidian_cost=Resources(ore=int(m.group(4)), clay=int(m.group(5))),
            geode_cost=Resources(ore=int(m.group(6)), obsidian=int(m.group(7)))
        )

    def calculate_max_geodes(self, minutes: int = 24, min_geode_count: int = 0) -> int:
        states: List[SearchNode] = [SearchNode.make(MiningState(), minutes)]
        history: Set[SearchNode] = set(states)
        best_geode_count: int = 0
        iteration = 0
        max_obsidian_bots = self.geode_cost.obsidian
        max_clay_bots = self.obsidian_cost.clay
        max_ore_bots = min(
            minutes - 3,
            (minutes - 2) * self.geode_cost.ore + max_obsidian_bots * self.obsidian_cost.ore
            + max_clay_bots * self.clay_cost.ore
        )
        tqdm.write(f"Max necessary bots: ore={max_ore_bots}, clay={max_clay_bots}, obsidian={max_obsidian_bots}")

        def add_state(s: MiningState):
            n = SearchNode.make(s, minutes)
            if n.geodes_upper_bound > best_geode_count and n.geodes_upper_bound >= min_geode_count and n not in history:
                heapq.heappush(states, n)
                history.add(n)

        while states:
            iteration += 1
            node = heapq.heappop(states)
            if node.geodes_upper_bound <= best_geode_count:
                break
            state = node.state
            if iteration % 100000 == 0:
                tqdm.write(f"iteration={iteration}\tqueue={len(states)}\tub={node.geodes_upper_bound}\t"
                           f"best={best_geode_count}")
                # tqdm.write(str(node.state))
            if node.state.minute >= minutes:
                if best_geode_count < 0:
                    best_geode_count = state.resources.geodes
                else:
                    best_geode_count = max(best_geode_count, state.resources.geodes)
                if best_geode_count <= 1:
                    break
                continue
            new_resources = node.state.resources + Resources(
                ore=state.ore_bots,
                clay=state.clay_bots,
                obsidian=state.obsidian_bots,
                geodes=state.geode_bots
            )
            # first option: do nothing
            add_state(MiningState(
                minute=state.minute + 1,
                resources=new_resources,
                ore_bots=state.ore_bots,
                clay_bots=state.clay_bots,
                obsidian_bots=state.obsidian_bots,
                geode_bots=state.geode_bots
            ))
            if state.ore_bots < max_ore_bots and self.ore_cost <= state.resources:
                # build an ore collecting robot
                add_state(MiningState(
                    minute=state.minute + 1,
                    resources=new_resources - self.ore_cost,
                    ore_bots=state.ore_bots + 1,
                    clay_bots=state.clay_bots,
                    obsidian_bots=state.obsidian_bots,
                    geode_bots=state.geode_bots
                ))
            if state.clay_bots < max_clay_bots and self.clay_cost <= state.resources:
                # build a clay collecting robot
                add_state(MiningState(
                    minute=state.minute + 1,
                    resources=new_resources - self.clay_cost,
                    ore_bots=state.ore_bots,
                    clay_bots=state.clay_bots + 1,
                    obsidian_bots=state.obsidian_bots,
                    geode_bots=state.geode_bots
                ))
            if state.obsidian_bots < max_obsidian_bots and self.obsidian_cost <= state.resources:
                # build an obsidian collecting robot
                add_state(MiningState(
                    minute=state.minute + 1,
                    resources=new_resources - self.obsidian_cost,
                    ore_bots=state.ore_bots,
                    clay_bots=state.clay_bots,
                    obsidian_bots=state.obsidian_bots + 1,
                    geode_bots=state.geode_bots
                ))
            if self.geode_cost <= state.resources:
                # build a geode collecting robot
                add_state(MiningState(
                    minute=state.minute + 1,
                    resources=new_resources - self.geode_cost,
                    ore_bots=state.ore_bots,
                    clay_bots=state.clay_bots,
                    obsidian_bots=state.obsidian_bots,
                    geode_bots=state.geode_bots + 1
                ))
        tqdm.write(f"Best geode quantity for blueprint {self.id_number}: {best_geode_count}")
        return best_geode_count

    def __str__(self):
        return f"Blueprint {self.id_number}: Each ore robot costs {self.ore_cost} ore. Each clay robot costs " \
               f"{self.clay_cost} ore. Each obsidian robot costs {self.obsidian_cost.ore} ore and " \
               f"{self.obsidian_cost.clay} clay. Each geode robot costs {self.geode_cost.ore} ore and " \
               f"{self.geode_cost.obsidian} obsidian."


def load(path: Path) -> Iterator[Blueprint]:
    with open(path, "r") as f:
        for line in f:
            yield Blueprint.parse(line)


@challenge(day=19)
def blueprint_quality(path: Path) -> int:
    return sum(
        blueprint.calculate_max_geodes() * blueprint.id_number
        for blueprint in tqdm(list(load(path)), unit="blueprint", leave=False)
    )
    best_quality = 0
    for blueprint in tqdm(list(reversed(list(load(path)))), unit="blueprint", leave=False):
        min_geode_count = best_quality // blueprint.id_number
        tqdm.write(f"Blueprint {blueprint.id_number} needs to produce at least {min_geode_count} geodes")
        m = blueprint.calculate_max_geodes(min_geode_count=min_geode_count)
        best_quality = max(best_quality, m * blueprint.id_number)
        tqdm.write(f"New max quality: {best_quality}")
    return best_quality
