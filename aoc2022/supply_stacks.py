from dataclasses import dataclass
import re
from typing import List, Tuple, Type

from . import challenge, Path

"""
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
"""


Stack: Type[List[str]] = list


MOVE_PATTERN: re.Pattern = re.compile(r"^\s*move\s+(\d+)\s+from\s+(\d+)\s+to\s+(\d+)\s*$")


@dataclass(frozen=True)
class Move:
    from_crate: int
    to_crate: int
    quantity: int

    @classmethod
    def load(cls, line: str) -> "Move":
        m = MOVE_PATTERN.match(line)
        if not m:
            raise ValueError(line)
        return cls(from_crate=int(m.group(2)) - 1, to_crate=int(m.group(3)) - 1, quantity=int(m.group(1)))

    def apply(self, stacks: List[Stack]) -> List[Stack]:
        result = list(stacks)
        result[self.from_crate] = Stack(result[self.from_crate])
        result[self.to_crate] = Stack(result[self.to_crate])
        if len(stacks[self.from_crate]) < self.quantity:
            raise ValueError(f"Insufficient crates in stack {self.from_crate} when applying {self!s}; "
                             f"stack only has {len(stacks[self.from_crate])} crates")
        for _ in range(self.quantity):
            to_move = result[self.from_crate].pop()
            result[self.to_crate].append(to_move)
        return result

    def __str__(self):
        return f"move {self.quantity} from {self.from_crate + 1} to {self.to_crate + 1}"


def load(path: Path) -> Tuple[List[Stack], List[Move]]:
    stacks: List[Stack] = []
    moves: List[Move] = []

    done_stacks = False

    with open(path, "r") as f:
        for line in f:
            if not done_stacks:
                if not line.strip():
                    done_stacks = True
                    continue
                stack_index = 0
                while line and not line.startswith("\n"):
                    if len(stacks) <= stack_index:
                        stacks.extend([Stack() for _ in range(stack_index - len(stacks) + 1)])
                    if line.startswith("["):
                        stacks[stack_index] = Stack([line[1]]) + stacks[stack_index]
                    line = line[4:]
                    stack_index += 1
            else:
                moves.append(Move.load(line))

    return stacks, moves


@challenge(day=5)
def top_stack(path: Path) -> str:
    stacks, moves = load(path)
    for move in moves:
        stacks = move.apply(stacks)
    return "".join(stack[-1] for stack in stacks)
