"""
--- Day 11: Monkey in the Middle ---
As you finally start making your way upriver, you realize your pack is much lighter than you remember. Just then, one of the items from your pack goes flying overhead. Monkeys are playing Keep Away with your missing things!

To get your stuff back, you need to be able to predict where the monkeys will throw your items. After some careful observation, you realize the monkeys operate based on how worried you are about each item.

You take some notes (your puzzle input) on the items each monkey currently has, how worried you are about those items, and how the monkey makes decisions based on your worry level. For example:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
Each monkey has several attributes:

Starting items lists your worry level for each item the monkey is currently holding in the order they will be inspected.
Operation shows how your worry level changes as that monkey inspects an item. (An operation like new = old * 5 means that your worry level after the monkey inspected the item is five times whatever your worry level was before inspection.)
Test shows how the monkey uses your worry level to decide where to throw an item next.
If true shows what happens with an item if the Test was true.
If false shows what happens with an item if the Test was false.
After each monkey inspects an item but before it tests your worry level, your relief that the monkey's inspection didn't damage the item causes your worry level to be divided by three and rounded down to the nearest integer.

The monkeys take turns inspecting and throwing items. On a single monkey's turn, it inspects and throws all of the items it is holding one at a time and in the order listed. Monkey 0 goes first, then monkey 1, and so on until each monkey has had one turn. The process of each monkey taking a single turn is called a round.

When a monkey throws an item to another monkey, the item goes on the end of the recipient monkey's list. A monkey that starts a round with no items could end up inspecting and throwing many items by the time its turn comes around. If a monkey is holding no items at the start of its turn, its turn ends.

In the above example, the first round proceeds as follows:

Monkey 0:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by 19 to 1501.
    Monkey gets bored with item. Worry level is divided by 3 to 500.
    Current worry level is not divisible by 23.
    Item with worry level 500 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 98.
    Worry level is multiplied by 19 to 1862.
    Monkey gets bored with item. Worry level is divided by 3 to 620.
    Current worry level is not divisible by 23.
    Item with worry level 620 is thrown to monkey 3.
Monkey 1:
  Monkey inspects an item with a worry level of 54.
    Worry level increases by 6 to 60.
    Monkey gets bored with item. Worry level is divided by 3 to 20.
    Current worry level is not divisible by 19.
    Item with worry level 20 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 65.
    Worry level increases by 6 to 71.
    Monkey gets bored with item. Worry level is divided by 3 to 23.
    Current worry level is not divisible by 19.
    Item with worry level 23 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 75.
    Worry level increases by 6 to 81.
    Monkey gets bored with item. Worry level is divided by 3 to 27.
    Current worry level is not divisible by 19.
    Item with worry level 27 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 6 to 80.
    Monkey gets bored with item. Worry level is divided by 3 to 26.
    Current worry level is not divisible by 19.
    Item with worry level 26 is thrown to monkey 0.
Monkey 2:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by itself to 6241.
    Monkey gets bored with item. Worry level is divided by 3 to 2080.
    Current worry level is divisible by 13.
    Item with worry level 2080 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 60.
    Worry level is multiplied by itself to 3600.
    Monkey gets bored with item. Worry level is divided by 3 to 1200.
    Current worry level is not divisible by 13.
    Item with worry level 1200 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 97.
    Worry level is multiplied by itself to 9409.
    Monkey gets bored with item. Worry level is divided by 3 to 3136.
    Current worry level is not divisible by 13.
    Item with worry level 3136 is thrown to monkey 3.
Monkey 3:
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 3 to 77.
    Monkey gets bored with item. Worry level is divided by 3 to 25.
    Current worry level is not divisible by 17.
    Item with worry level 25 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 500.
    Worry level increases by 3 to 503.
    Monkey gets bored with item. Worry level is divided by 3 to 167.
    Current worry level is not divisible by 17.
    Item with worry level 167 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 620.
    Worry level increases by 3 to 623.
    Monkey gets bored with item. Worry level is divided by 3 to 207.
    Current worry level is not divisible by 17.
    Item with worry level 207 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 1200.
    Worry level increases by 3 to 1203.
    Monkey gets bored with item. Worry level is divided by 3 to 401.
    Current worry level is not divisible by 17.
    Item with worry level 401 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 3136.
    Worry level increases by 3 to 3139.
    Monkey gets bored with item. Worry level is divided by 3 to 1046.
    Current worry level is not divisible by 17.
    Item with worry level 1046 is thrown to monkey 1.
After round 1, the monkeys are holding items with these worry levels:

Monkey 0: 20, 23, 27, 26
Monkey 1: 2080, 25, 167, 207, 401, 1046
Monkey 2:
Monkey 3:
Monkeys 2 and 3 aren't holding any items at the end of the round; they both inspected items during the round and threw them all before the round ended.

This process continues for a few more rounds:

After round 2, the monkeys are holding items with these worry levels:
Monkey 0: 695, 10, 71, 135, 350
Monkey 1: 43, 49, 58, 55, 362
Monkey 2:
Monkey 3:

After round 3, the monkeys are holding items with these worry levels:
Monkey 0: 16, 18, 21, 20, 122
Monkey 1: 1468, 22, 150, 286, 739
Monkey 2:
Monkey 3:

After round 4, the monkeys are holding items with these worry levels:
Monkey 0: 491, 9, 52, 97, 248, 34
Monkey 1: 39, 45, 43, 258
Monkey 2:
Monkey 3:

After round 5, the monkeys are holding items with these worry levels:
Monkey 0: 15, 17, 16, 88, 1037
Monkey 1: 20, 110, 205, 524, 72
Monkey 2:
Monkey 3:

After round 6, the monkeys are holding items with these worry levels:
Monkey 0: 8, 70, 176, 26, 34
Monkey 1: 481, 32, 36, 186, 2190
Monkey 2:
Monkey 3:

After round 7, the monkeys are holding items with these worry levels:
Monkey 0: 162, 12, 14, 64, 732, 17
Monkey 1: 148, 372, 55, 72
Monkey 2:
Monkey 3:

After round 8, the monkeys are holding items with these worry levels:
Monkey 0: 51, 126, 20, 26, 136
Monkey 1: 343, 26, 30, 1546, 36
Monkey 2:
Monkey 3:

After round 9, the monkeys are holding items with these worry levels:
Monkey 0: 116, 10, 12, 517, 14
Monkey 1: 108, 267, 43, 55, 288
Monkey 2:
Monkey 3:

After round 10, the monkeys are holding items with these worry levels:
Monkey 0: 91, 16, 20, 98
Monkey 1: 481, 245, 22, 26, 1092, 30
Monkey 2:
Monkey 3:

...

After round 15, the monkeys are holding items with these worry levels:
Monkey 0: 83, 44, 8, 184, 9, 20, 26, 102
Monkey 1: 110, 36
Monkey 2:
Monkey 3:

...

After round 20, the monkeys are holding items with these worry levels:
Monkey 0: 10, 12, 14, 26, 34
Monkey 1: 245, 93, 53, 199, 115
Monkey 2:
Monkey 3:
Chasing all of the monkeys at once is impossible; you're going to have to focus on the two most active monkeys if you want any hope of getting your stuff back. Count the total number of times each monkey inspects items over 20 rounds:

Monkey 0 inspected items 101 times.
Monkey 1 inspected items 95 times.
Monkey 2 inspected items 7 times.
Monkey 3 inspected items 105 times.
In this example, the two most active monkeys inspected items 101 and 105 times. The level of monkey business in this situation can be found by multiplying these together: 10605.

Figure out which monkeys to chase by counting how many items they inspect over 20 rounds. What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
"""

from enum import Enum
import heapq
import math
from typing import Callable, Dict, Iterable, Iterator, List, Optional, TextIO, Tuple

from tqdm import trange

from . import challenge, Path


class Operator(Enum):
    ADD = ("+", lambda x, y: x + y)
    MULTIPLY = ("*", lambda x, y: x * y)

    def __init__(self, symbol: str, function: Callable[[int, int], int]):
        self.symbol: str = symbol
        self.function: Callable[[int, int], int] = function


class Monkey:
    def __init__(
            self,
            number: int,
            items: Iterable[int],
            operator: Operator,
            operand: Optional[int],
            divisible_by: int,
            if_true: int,
            if_false: int
    ):
        self.number: int = number
        self.items: List[int] = list(items)
        self.operator: Operator = operator
        self.operand: Optional[int] = operand
        self.divisible_by: int = divisible_by
        self.if_true: int = if_true
        self.if_false: int = if_false
        self.num_items_inspected: int = 0
        self.worry_divisor: int = 3

    def next(self, worry_level: int, lcm: Optional[int] = None) -> Tuple[int, int]:
        operand = self.operand
        if operand is None:
            operand = worry_level
        new_level = self.operator.function(worry_level, operand) // self.worry_divisor
        if lcm is not None:
            new_level %= lcm
        if new_level % self.divisible_by == 0:
            return new_level, self.if_true
        else:
            return new_level, self.if_false

    def take_turn(self, monkeys: Dict[int, "Monkey"], lcm: Optional[int] = None):
        for worry_level in self.items:
            self.num_items_inspected += 1
            new_level, new_monkey = self.next(worry_level, lcm)
            monkeys[new_monkey].items.append(new_level)
        self.items = []

    @classmethod
    def parse(cls, stream: TextIO) -> "Monkey":
        while True:
            monkey = stream.readline()
            if not monkey:
                raise ValueError()
            monkey = monkey.strip()
            if monkey:
                break
        if not monkey.startswith("Monkey ") or not monkey.endswith(":"):
            raise ValueError(monkey)
        monkey_id = int(monkey[len("Monkey "):-1])
        items = stream.readline().strip()
        if not items.startswith("Starting items: "):
            raise ValueError(items)
        starting_items = list(map(int, items[len("Starting items: "):].split(",")))
        operation = stream.readline().strip()
        operator_prefix = "Operation: new = old "
        if not operation.startswith(operator_prefix):
            raise ValueError(operation)
        operator_str = operation[len(operator_prefix)]
        for operator in Operator:
            if operator.symbol == operator_str:
                break
        else:
            raise ValueError(operation)
        operand_str = operation[len(operator_prefix) + 1:].strip()
        if operand_str == "old":
            operand: Optional[int] = None
        else:
            operand = int(operand_str)
        test = stream.readline().strip()
        if not test.startswith("Test: divisible by "):
            raise ValueError(test)
        divisible_by = int(test[len("Test: divisible by "):])
        if_true_str = stream.readline().strip()
        if not if_true_str.startswith("If true: throw to monkey "):
            raise ValueError(if_true_str)
        if_true = int(if_true_str[len("If true: throw to monkey "):])
        if_false_str = stream.readline().strip()
        if not if_false_str.startswith("If false: throw to monkey "):
            raise ValueError(if_false_str)
        if_false = int(if_false_str[len("If false: throw to monkey "):])
        return Monkey(
            number=monkey_id,
            items=starting_items,
            operator=operator,
            operand=operand,
            divisible_by=divisible_by,
            if_true=if_true,
            if_false=if_false
        )

    def __str__(self):
        return f"""Monkey {self.number}
  Items: {', '.join(map(str, self.items))}
  Operation: new = old {self.operator.value} {[self.operator, "old"][self.operator is None]}
  Test: divisible by {self.divisible_by}
    If true: throw to monkey {self.if_true}
    If false: throw to monkey {self.if_false}
"""


def load(path: Path) -> Dict[int, Monkey]:
    monkeys: Dict[int, Monkey] = {}
    with open(path, "r") as f:
        while True:
            try:
                monkey = Monkey.parse(f)
                monkeys[monkey.number] = monkey
            except ValueError as e:
                break
    return monkeys


@challenge(day=11)
def monkey_business(path: Path) -> int:
    monkeys = load(path)
    for _ in trange(20, desc="simulating", unit="rounds", leave=False):
        for i in trange(len(monkeys), desc="running round", unit="monkeys", leave=False):
            monkeys[i].take_turn(monkeys)
    top_two = heapq.nlargest(2, monkeys.values(), key=lambda m: m.num_items_inspected)
    return top_two[0].num_items_inspected * top_two[1].num_items_inspected


"""
--- Part Two ---
You're worried you might not ever get your items back. So worried, in fact, that your relief that a monkey's inspection didn't damage an item no longer causes your worry level to be divided by three.

Unfortunately, that relief was all that was keeping your worry levels from reaching ridiculous levels. You'll need to find another way to keep your worry levels manageable.

At this rate, you might be putting up with these monkeys for a very long time - possibly 10000 rounds!

With these new rules, you can still figure out the monkey business after 10000 rounds. Using the same example above:

== After round 1 ==
Monkey 0 inspected items 2 times.
Monkey 1 inspected items 4 times.
Monkey 2 inspected items 3 times.
Monkey 3 inspected items 6 times.

== After round 20 ==
Monkey 0 inspected items 99 times.
Monkey 1 inspected items 97 times.
Monkey 2 inspected items 8 times.
Monkey 3 inspected items 103 times.

== After round 1000 ==
Monkey 0 inspected items 5204 times.
Monkey 1 inspected items 4792 times.
Monkey 2 inspected items 199 times.
Monkey 3 inspected items 5192 times.

== After round 2000 ==
Monkey 0 inspected items 10419 times.
Monkey 1 inspected items 9577 times.
Monkey 2 inspected items 392 times.
Monkey 3 inspected items 10391 times.

== After round 3000 ==
Monkey 0 inspected items 15638 times.
Monkey 1 inspected items 14358 times.
Monkey 2 inspected items 587 times.
Monkey 3 inspected items 15593 times.

== After round 4000 ==
Monkey 0 inspected items 20858 times.
Monkey 1 inspected items 19138 times.
Monkey 2 inspected items 780 times.
Monkey 3 inspected items 20797 times.

== After round 5000 ==
Monkey 0 inspected items 26075 times.
Monkey 1 inspected items 23921 times.
Monkey 2 inspected items 974 times.
Monkey 3 inspected items 26000 times.

== After round 6000 ==
Monkey 0 inspected items 31294 times.
Monkey 1 inspected items 28702 times.
Monkey 2 inspected items 1165 times.
Monkey 3 inspected items 31204 times.

== After round 7000 ==
Monkey 0 inspected items 36508 times.
Monkey 1 inspected items 33488 times.
Monkey 2 inspected items 1360 times.
Monkey 3 inspected items 36400 times.

== After round 8000 ==
Monkey 0 inspected items 41728 times.
Monkey 1 inspected items 38268 times.
Monkey 2 inspected items 1553 times.
Monkey 3 inspected items 41606 times.

== After round 9000 ==
Monkey 0 inspected items 46945 times.
Monkey 1 inspected items 43051 times.
Monkey 2 inspected items 1746 times.
Monkey 3 inspected items 46807 times.

== After round 10000 ==
Monkey 0 inspected items 52166 times.
Monkey 1 inspected items 47830 times.
Monkey 2 inspected items 1938 times.
Monkey 3 inspected items 52013 times.
After 10000 rounds, the two most active monkeys inspected items 52166 and 52013 times. Multiplying these together, the level of monkey business in this situation is now 2713310158.

Worry levels are no longer divided by three after each item is inspected; you'll need to find another way to keep your worry levels manageable. Starting again from the initial state in your puzzle input, what is the level of monkey business after 10000 rounds?
"""


@challenge(day=11)
def over_nine_thousand_rounds(path: Path) -> int:
    monkeys = load(path)
    for monkey in monkeys.values():
        monkey.worry_divisor = 1
    lcm = math.lcm(*(i for m in monkeys.values() for i in m.items))
    for _ in trange(10000, desc="simulating", unit="rounds", leave=False):
        for i in trange(len(monkeys), desc="running round", unit="monkeys", leave=False):
            monkeys[i].take_turn(monkeys, lcm=lcm)
    top_two = heapq.nlargest(2, monkeys.values(), key=lambda m: m.num_items_inspected)
    return top_two[0].num_items_inspected * top_two[1].num_items_inspected
