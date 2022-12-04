from typing import FrozenSet, Iterable, Iterator, Tuple

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


"""
--- Part Two ---
As you finish identifying the misplaced items, the Elves come to you with another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right one is by finding the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type. So, in the above example, the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. In the second group, their badge item type must be Z.

Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for the first group and 52 (Z) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
"""


def load_groups(path: Path) -> Iterator[Tuple[Rucksack, Rucksack, Rucksack]]:
    with open(path, "r") as f:
        line_group = []
        for line in f:
            line_group.append(line.strip())
            if len(line_group) == 3:
                yield map(Rucksack.load, line_group)
                line_group = []
        assert not line_group


@challenge(day=3)
def elf_groups(path: Path) -> int:
    total = 0
    for r1, r2, r3 in load_groups(path):
        common_value = (r1.compartment1 | r1.compartment2) & (r2.compartment1 | r2.compartment2) \
                       & (r3.compartment1 | r3.compartment2)
        assert len(common_value) == 1
        total += next(iter(common_value)).priority
    return total
