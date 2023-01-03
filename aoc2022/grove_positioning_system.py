from typing import Iterable, List, Optional

from tqdm import trange

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

    def decrypt(self, num_mixings: int = 1):
        # print("Initial arrangement:")
        # print(", ".join(map(str, self.sequence)))
        # print("")
        for _ in trange(num_mixings, desc="mixing", leave=False, unit="mixes"):
            for i in trange(len(self.indexes), leave=False, unit="indexes"):
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


"""--- Part Two ---
The grove coordinate values seem nonsensical. While you ponder the mysteries of Elf encryption, you suddenly remember the rest of the decryption routine you overheard back at camp.

First, you need to apply the decryption key, 811589153. Multiply each number by the decryption key before you begin; this will produce the actual list of numbers to mix.

Second, you need to mix the list of numbers ten times. The order in which the numbers are mixed does not change during mixing; the numbers are still moved in the order they appeared in the original, pre-mixed list. (So, if -3 appears fourth in the original list of numbers to mix, -3 will be the fourth number to move during each round of mixing.)

Using the same example as above:

Initial arrangement:
811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612

After 1 round of mixing:
0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153

After 2 rounds of mixing:
0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153

After 3 rounds of mixing:
0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459

After 4 rounds of mixing:
0, 1623178306, -2434767459, 811589153, 2434767459, 3246356612, -1623178306

After 5 rounds of mixing:
0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459

After 6 rounds of mixing:
0, 811589153, -1623178306, 3246356612, -2434767459, 1623178306, 2434767459

After 7 rounds of mixing:
0, -2434767459, 2434767459, 1623178306, -1623178306, 811589153, 3246356612

After 8 rounds of mixing:
0, 1623178306, 3246356612, 811589153, -2434767459, 2434767459, -1623178306

After 9 rounds of mixing:
0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306

After 10 rounds of mixing:
0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153
The grove coordinates can still be found in the same way. Here, the 1000th number after 0 is 811589153, the 2000th is 2434767459, and the 3000th is -1623178306; adding these together produces 1623178306.

Apply the decryption key and mix your encrypted file ten times. What is the sum of the three numbers that form the grove coordinates?
"""


@challenge(day=20)
def with_decryption_key(path: Path) -> int:
    with open(path, "r") as f:
        ciphertext = Ciphertext((int(line) * 811589153 for line in f))
    ciphertext.decrypt(num_mixings=10)
    final_zero_index = ciphertext.indexes[ciphertext.zero_index]
    return ciphertext[final_zero_index + 1000] + ciphertext[final_zero_index + 2000] \
        + ciphertext[final_zero_index + 3000]
