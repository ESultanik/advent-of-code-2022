"""
--- Day 18: Boiling Boulders ---
You and the elephants finally reach fresh air. You've emerged near the base of a large volcano that seems to be actively erupting! Fortunately, the lava seems to be flowing away from you and toward the ocean.

Bits of lava are still being ejected toward you, so you're sheltering in the cavern exit a little longer. Outside the cave, you can see the lava landing in a pond and hear it loudly hissing as it solidifies.

Depending on the specific compounds in the lava and speed at which it cools, it might be forming obsidian! The cooling rate should be based on the surface area of the lava droplets, so you take a quick scan of a droplet as it flies past you (your puzzle input).

Because of how quickly the lava is moving, the scan isn't very good; its resolution is quite low and, as a result, it approximates the shape of the lava droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

To approximate the surface area, count the number of sides of each cube that are not immediately connected to another cube. So, if your scan were only two adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side covered and five sides exposed, a total surface area of 10 sides.

Here's a larger example:

2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
In the above example, after counting up all the sides that aren't connected to another cube, the total surface area is 64.

What is the surface area of your scanned lava droplet?
"""

from typing import Dict, Iterable, Iterator, Set, Tuple

from tqdm import tqdm

from . import challenge, Path


Voxel = Tuple[int, int, int]


class Droplet:
    def __init__(self, cubes: Iterable[Voxel]):
        self.cubes: Dict[int, Dict[int, Set[int]]] = {}
        self._size: int = 0
        for x, y, z in cubes:
            if x not in self.cubes:
                row = {}
                self.cubes[x] = row
            else:
                row = self.cubes[x]
            if y not in row:
                col = set()
                row[y] = col
            else:
                col = row[y]
            if z not in col:
                col.add(z)
                self._size += 1
        self.convex_hull: Tuple[Voxel, Voxel] = (
            (
                min(x for x, _, _ in self),
                min(y for _, y, _ in self),
                min(z for _, _, z in self)
            ),
            (
                max(x for x, _, _ in self),
                max(y for _, y, _ in self),
                max(z for _, _, z in self)
            ),
        )
        self._exterior: Set[Voxel] = set()

    def __len__(self):
        return self._size

    def __iter__(self) -> Iterator[Voxel]:
        for x, row in self.cubes.items():
            for y, col in row.items():
                yield from ((x, y, z) for z in col)

    def __contains__(self, cube: Voxel):
        x, y, z = cube
        return x in self.cubes and y in self.cubes[x] and z in self.cubes[x][y]

    @staticmethod
    def neighbors(cube: Voxel) -> Iterator[Voxel]:
        x, y, z = cube
        for x_delta in (-1, 0, 1):
            next_x = x + x_delta
            for y_delta in (-1, 0, 1):
                next_y = y + y_delta
                for z_delta in (-1, 0, 1):
                    if abs(x_delta) + abs(y_delta) + abs(z_delta) == 1:
                        yield next_x, next_y, z + z_delta

    def is_exterior(self, cube: Voxel) -> bool:
        # find a path to a point outside the convex hull

        stack = [cube]
        history = set(stack)
        while stack:
            cube = stack.pop()
            x, y, z = cube
            (min_x, min_y, min_z), (max_x, max_y, max_z) = self.convex_hull
            if x < min_x or x > max_x or y < min_y or y > max_y or z < min_z or z > max_z:
                return True
            neighbors = {n for n in Droplet.neighbors(cube) if n not in history and n not in self}
            history |= neighbors
            stack.extend(neighbors)
        return False

    def surface_area(self, exterior_only: bool = False) -> int:
        total = 0
        for cube in tqdm(self, leave=False, unit="cube"):
            for neighbor in Droplet.neighbors(cube):
                if neighbor not in self and (not exterior_only or self.is_exterior(neighbor)):
                    total += 1
        return total

    @classmethod
    def load(cls, path: Path) -> "Droplet":
        with open(path, "r") as f:
            return cls(
                (map(int, line.strip().split(",")) for line in f)  # type: ignore
            )


@challenge(day=18)
def surface_area(path: Path) -> int:
    return Droplet.load(path).surface_area()


"""
--- Part Two ---
Something seems off about your calculation. The cooling rate depends on exterior surface area, but your calculation also included the surface area of air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

What is the exterior surface area of your scanned lava droplet?
"""


@challenge(day=18)
def exterior_surface_area(path: Path) -> int:
    return Droplet.load(path).surface_area(exterior_only=True)
