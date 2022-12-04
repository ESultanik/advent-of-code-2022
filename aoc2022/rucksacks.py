from typing import FrozenSet, Iterable, Iterator

from . import challenge, Path

"""
--- Day 3: Rucksack Reorganization ---
One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both compartments is lowercase p.
The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L.
The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
The fourth rucksack's compartments only share item type v.
The fifth rucksack's compartments only share item type t.
The sixth rucksack's compartments only share item type s.
To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.
In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
"""


class Item:
    def __init__(self, item_type: str):
        if len(item_type) != 1:
            raise ValueError(item_type)
        self.item_type: str = item_type

    def __eq__(self, other):
        return isinstance(other, Item) and self.item_type == other.item_type

    def __hash__(self):
        return hash(self.item_type)

    def __lt__(self, other):
        return isinstance(other, Item) and self.priority < other.priority

    @property
    def priority(self) -> int:
        if self.item_type.lower() == self.item_type:
            return ord(self.item_type) - ord('a') + 1
        else:
            return ord(self.item_type) - ord('A') + 27


class Rucksack:
    def __init__(self, compartment1: Iterable[Item], compartment2: Iterable[Item]):
        self.compartment1: FrozenSet[Item] = frozenset(compartment1)
        self.compartment2: FrozenSet[Item] = frozenset(compartment2)

    @classmethod
    def load(cls, items: Iterable[str]) -> "Rucksack":
        items = list(items)
        if len(items) % 2 != 0:
            raise ValueError("The number of items must be even!")
        midpoint = len(items)//2
        return cls(compartment1=map(Item, items[:midpoint]), compartment2=map(Item, items[midpoint:]))


def load_rucksacks(path: Path) -> Iterator[Rucksack]:
    with open(path, "r") as f:
        for line in f:
            yield Rucksack.load(line.strip())


@challenge(day=3)
def rucksack_reorganiztion(path: Path) -> int:
    return sum(next(iter(r.compartment1 & r.compartment2)).priority for r in load_rucksacks(path))
