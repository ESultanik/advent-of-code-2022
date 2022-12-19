from typing import Dict, Iterable, Iterator, Set, Tuple

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

    def __len__(self):
        return self._size

    def __iter__(self) -> Iterator[Voxel]:
        for x, row in self.cubes.items():
            for y, col in row.items():
                yield from ((x, y, z) for z in col)

    def __contains__(self, cube: Voxel):
        x, y, z = cube
        return x in self.cubes and y in self.cubes[x] and z in self.cubes[x][y]

    def surface_area(self) -> int:
        total = 0
        for x, y, z in self:
            for x_delta in (-1, 0, 1):
                next_x = x + x_delta
                for y_delta in (-1, 0, 1):
                    next_y = y + y_delta
                    for z_delta in (-1, 0, 1):
                        if abs(x_delta) + abs(y_delta) + abs(z_delta) > 1:
                            continue
                        elif (next_x, next_y, z + z_delta) not in self:
                            total += 1
        return total


@challenge(day=18)
def surface_area(path: Path) -> int:
    with open(path, "r") as f:
        droplet = Droplet(
            (map(int, line.strip().split(",")) for line in f)  # type: ignore
        )
    return droplet.surface_area()
