from typing import Dict, Iterable, List, Optional

from . import challenge, Path


class Ciphertext:
    def __init__(self, sequence: Iterable[int], zero_index: Optional[int] = None):
        self.sequence: List[int] = list(sequence)
        self.indexes: List[int] = list(range(len(self.sequence)))
        if zero_index is not None:
            if self.sequence[zero_index] != 0:
                raise ValueError(f"Zero index {zero_index} is incorrect!")
            self.zero_index: int = zero_index
        else:
            self.zero_index = self.sequence.index(0)

    def __getitem__(self, index: int) -> int:
        return self.sequence[index % len(self.sequence)]

    def mix(self, original_index: int):
        current_index = self.indexes[original_index]
        value = self.sequence[current_index]
        new_index = (current_index + value) % (len(self.sequence) - 1)
        # if new_index == 0:
        #     print(f"{value} moves before {self.sequence[0]}")
        # else:
        #     print(f"{value} moves between {self.sequence[new_index]} and {self.sequence[new_index + 1]}")
        if new_index < current_index:
            self.sequence = self.sequence[:new_index] + [value] + \
                            self.sequence[new_index:current_index] + self.sequence[current_index+1:]
            for oi, ci in list(enumerate(self.indexes)):
                if new_index <= ci < current_index:
                    self.indexes[oi] = ci + 1
        elif new_index > current_index:
            self.sequence = self.sequence[:current_index] + self.sequence[current_index+1:new_index + 1] + \
                            [value] + self.sequence[new_index + 1:]
            for oi, ci in list(enumerate(self.indexes)):
                if current_index < ci <= new_index:
                    self.indexes[oi] = ci - 1
        self.indexes[original_index] = new_index

    def decrypt(self):
        # print("Initial arrangement:")
        # print(", ".join(map(str, self.sequence)))
        # print("")
        for i in range(len(self.indexes)):
            self.mix(i)
            # print(", ".join(map(str, self.sequence)))
            # print("")


@challenge(day=20)
def grove_coordinates(path: Path) -> int:
    with open(path, "r") as f:
        ciphertext = Ciphertext(map(int, f))
    ciphertext.decrypt()
    final_zero_index = ciphertext.indexes[ciphertext.zero_index]
    return ciphertext[final_zero_index + 1000] + ciphertext[final_zero_index + 2000] \
        + ciphertext[final_zero_index + 3000]