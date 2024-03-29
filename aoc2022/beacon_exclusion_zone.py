"""
--- Day 15: Beacon Exclusion Zone ---
You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels. You don't have time to search them all, but you don't need to: your pack contains a set of deployable sensors that you imagine were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the source of the distress signal to use them. You pull the emergency sensor system out of your pack, hit the big button on top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins monitoring for the nearest signal source beacon. Sensors and beacons always exist at integer coordinates. Each sensor knows its own position and can determine the position of a beacon precisely; however, sensors can only lock on to the one beacon closest to the sensor as measured by the Manhattan distance. (There is never a tie where two beacons are the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input). For example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the sensor at 9,16, the closest beacon to it is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This isn't necessarily a comprehensive map of all beacons in the area, though. Because each sensor only identifies its closest beacon, if a sensor detects a beacon, you know there are no other beacons that close or closer to that sensor. There could still be beacons that just happen to not be the closest beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This sensor's closest beacon is at 2,10, and so you know there are no beacons that close or closer (in any positions marked #).

None of the detected beacons seem to be producing the distress signal, so you'll need to work out where the distress beacon is by working out where it isn't. For now, keep things simple by counting the positions where a beacon cannot possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the example above and, just in the row where y=10, you'd like to count the number of positions a beacon cannot possibly exist. The coverage from all sensors near that row looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.
In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.

Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a beacon?
"""

from dataclasses import dataclass
import re
from typing import Dict, Iterator

from intervaltree import Interval, IntervalTree
from tqdm import tqdm, trange

from . import challenge, Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def distance_to(self, point: "Point") -> int:
        return abs(self.x - point.x) + abs(self.y - point.y)


SENSOR_PATTERN: re.Pattern = re.compile(
    r"\s*Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)\s*"
)


@dataclass(frozen=True)
class Sensor:
    location: Point
    closest_beacon: Point

    @property
    def closest_beacon_distance(self) -> int:
        return self.location.distance_to(self.closest_beacon)

    def can_contain_beacon(self, point: Point) -> bool:
        if self.closest_beacon == point:
            return True
        elif self.location == point:
            return False
        else:
            return self.location.distance_to(point) > self.closest_beacon_distance

    def excluded_x_values(self, in_row: int) -> IntervalTree:
        y_delta = abs(self.location.y - in_row)
        x_delta = self.closest_beacon_distance - y_delta
        if x_delta < 0:
            # the row is too far away from our sensor
            return IntervalTree()
        tree = IntervalTree([Interval(self.location.x - x_delta, self.location.x + x_delta + 1)])
        if y_delta == 0:
            tree.addi(self.location.x, self.location.x + 1)
        if in_row == self.closest_beacon.y:
            tree.chop(self.closest_beacon.x, self.closest_beacon.x + 1)
        return tree

    @property
    def min_x(self) -> int:
        return self.location.x - self.closest_beacon_distance

    @property
    def max_x(self) -> int:
        return self.location.x + self.closest_beacon_distance

    @property
    def min_y(self) -> int:
        return self.location.y - self.closest_beacon_distance

    @property
    def max_y(self) -> int:
        return self.location.y + self.closest_beacon_distance

    @classmethod
    def parse(cls, line: str) -> "Sensor":
        m = SENSOR_PATTERN.match(line)
        if not m:
            raise ValueError(line)
        return Sensor(
            location=Point(x=int(m.group(1)), y=int(m.group(2))),
            closest_beacon=Point(x=int(m.group(3)), y=int(m.group(4)))
        )


def load(path: Path) -> Iterator[Sensor]:
    with open(path, "r") as f:
        for line in f:
            yield Sensor.parse(line)


@challenge(day=15)
def row_two_million(path: Path) -> int:
    excluded = IntervalTree()
    for sensor in load(path):
        excluded |= sensor.excluded_x_values(2000000)
    excluded.merge_overlaps()
    return sum(
        interval.end - interval.begin
        for interval in excluded
    )


"""
--- Part Two ---
Your handheld device indicates that the distress signal is coming from a beacon nearby. The distress beacon is not detected by any sensor, but the distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.

To isolate the distress beacon's signal, you need to determine its tuning frequency, which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.

In the example above, the search space is smaller: instead, the x and y coordinates can each be at most 20. With this reduced search area, there is only a single position that could have a beacon: x=14, y=11. The tuning frequency for this distress beacon is 56000011.

Find the only possible position for the distress beacon. What is its tuning frequency?
"""


@challenge(day=15)
def tuning_frequency(path: Path) -> int:
    max_value = 4000000
    sensors = list(load(path))
    known_beacon_positions = {
        (sensor.closest_beacon.x, sensor.closest_beacon.y)
        for sensor in sensors
    }
    for y in trange(0, max_value + 1, desc="scanning", unit="row", leave=False):
        excluded = IntervalTree()
        for sensor in sensors:
            if sensor.min_y <= y <= sensor.max_y:
                excluded |= sensor.excluded_x_values(in_row=y)
        excluded.merge_overlaps()
        possible_locations = IntervalTree([Interval(0, max_value + 1)])
        for interval in excluded:
            if interval.end > 0 or interval.begin <= max_value:
                possible_locations.chop(interval.begin, interval.end)
        for interval in possible_locations:
            for x in range(interval.begin, interval.end):
                if (x, y) not in known_beacon_positions:
                    tqdm.write(f"Beacon: x={x}, y={y}")
                    return x * 4000000 + y
    else:
        raise ValueError("No solution!")
