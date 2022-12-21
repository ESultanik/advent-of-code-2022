"""
--- Day 21: Monkey Math ---
The monkeys are back! You're worried they're going to try to steal your stuff again, but it seems like they're just holding their ground and making various monkey noises at you.

Eventually, one of the elephants realizes you don't speak monkey and comes over to interpret. As it turns out, they overheard you talking about trying to find the grove; they can show you a shortcut if you answer their riddle.

Each monkey is given a job: either to yell a specific number or to yell the result of a math operation. All of the number-yelling monkeys know their number from the start; however, the math operation monkeys need to wait for two other monkeys to yell a number, and those two other monkeys might also be waiting on other monkeys.

Your job is to work out the number the monkey named root will yell before the monkeys figure it out themselves.

For example:

root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
Each line contains the name of a monkey, a colon, and then the job of that monkey:

A lone number means the monkey's job is simply to yell that number.
A job like aaaa + bbbb means the monkey waits for monkeys aaaa and bbbb to yell each of their numbers; the monkey then yells the sum of those two numbers.
aaaa - bbbb means the monkey yells aaaa's number minus bbbb's number.
Job aaaa * bbbb will yell aaaa's number multiplied by bbbb's number.
Job aaaa / bbbb will yell aaaa's number divided by bbbb's number.
So, in the above example, monkey drzm has to wait for monkeys hmdt and zczc to yell their numbers. Fortunately, both hmdt and zczc have jobs that involve simply yelling a single number, so they do this immediately: 32 and 2. Monkey drzm can then yell its number by finding 32 minus 2: 30.

Then, monkey sjmn has one of its numbers (30, from monkey drzm), and already has its other number, 5, from dbpl. This allows it to yell its own number by finding 30 multiplied by 5: 150.

This process continues until root yells a number: 152.

However, your actual situation involves considerably more monkeys. What number will the monkey named root yell?
"""

from enum import Enum
from typing import Callable, Dict, List, Optional, Set, Union

from . import challenge, Path


Operand = Union["Symbol", int, "Expression"]


class Symbol:
    def __init__(self, name: Union[str, "Symbol"]):
        if isinstance(name, str):
            self.name: str = name
        else:
            self.name = name.name

    def simplify(self, assignments: Optional["KnowledgeBase"] = None) -> Operand:
        if assignments is not None:
            return self.resolve(assignments)
        return self

    def resolve(self, assignments: "KnowledgeBase") -> Operand:
        op = self
        while op in assignments:
            op = assignments[op]
            if op == self:
                return op
            if isinstance(op, Expression):
                op = op.resolve(assignments)
        return op

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Symbol) and other.name == self.name

    def __add__(self, other: Operand) -> "Expression":
        return Expression(lhs=self, operator=Operator.ADD, rhs=other)

    __radd__ = __add__

    def __sub__(self, other: Operand) -> "Expression":
        return Expression(lhs=self, operator=Operator.SUBTRACT, rhs=other)

    def __rsub__(self, other: Operand) -> "Expression":
        return Expression(lhs=other, operator=Operator.SUBTRACT, rhs=self)

    def __mul__(self, other: Operand) -> "Expression":
        return Expression(lhs=self, operator=Operator.MULTIPLY, rhs=other)

    __rmul__ = __mul__

    def __floordiv__(self, other: Operand) -> "Expression":
        return Expression(lhs=self, operator=Operator.DIVIDE, rhs=other)

    def __rfloordiv__(self, other: Operand) -> "Expression":
        return Expression(lhs=other, operator=Operator.DIVIDE, rhs=self)

    def __str__(self):
        return self.name


class Operator(Enum):
    ADD = ("+", lambda a, b: a + b)
    SUBTRACT = ("-", lambda a, b: a - b)
    MULTIPLY = ("*", lambda a, b: a * b)
    DIVIDE = ("/", lambda a, b: a // b)
    EQUALS = ("==", lambda a, b: Expression(lhs=a, operator=Operator.EQUALS, rhs=b))

    def __init__(self, symbol: str, operator: Callable[[Operand, Operand], Operand]):
        self.symbol: str = symbol
        self.execute: Callable[[Operand, Operand], Operand] = operator


class Expression:
    def __init__(self, lhs: Operand, operator: Operator, rhs: Operand):
        self.lhs: Operand = lhs
        self.operator: Operator = operator
        self.rhs: Operand = rhs

    def __eq__(self, other) -> "Expression":
        if not isinstance(other, Expression) or self.operator != other.operator:
            return False
        elif self.lhs == other.lhs and self.rhs == other.rhs:
            return True
        elif self.operator == Operator.DIVIDE and self.operator == Operator.MULTIPLY:
            return False
        return self.lhs == other.rhs and self.rhs == other.lhs

    def __add__(self, other: Operand) -> "Expression":
        return Expression(self, Operator.ADD, other)

    __radd__ = __add__

    def __sub__(self, other: Operand) -> "Expression":
        return Expression(self, Operator.SUBTRACT, other)

    def __rsub__(self, other: Operand) -> "Expression":
        return Expression(other, Operator.SUBTRACT, self)

    def __mul__(self, other: Operand) -> "Expression":
        return Expression(self, Operator.MULTIPLY, other)

    __rmul__ = __mul__

    def __floordiv__(self, other: Operand) -> "Expression":
        return Expression(self, Operator.DIVIDE, other)

    def __rfloordiv__(self, other: Operand) -> "Expression":
        return Expression(other, Operator.DIVIDE, self)

    def simplify(self, assignments: Optional["KnowledgeBase"] = None) -> Operand:
        if isinstance(self.lhs, int):
            lhs: Operand = self.lhs
        else:
            lhs = self.lhs.simplify(assignments)
        if isinstance(self.rhs, int):
            rhs: Operand = self.rhs
        else:
            rhs = self.rhs.simplify(assignments)
        if isinstance(lhs, int) and isinstance(rhs, int):
            return self.operator.execute(lhs, rhs)
        return Expression(lhs=lhs, operator=self.operator, rhs=rhs)

    def resolve(self, assignments: "KnowledgeBase") -> "Expression":
        if isinstance(self.lhs, int):
            lhs: Operand = self.lhs
        else:
            lhs = self.lhs.resolve(assignments)
        if isinstance(self.rhs, int):
            rhs: Operand = self.rhs
        else:
            rhs = self.rhs.resolve(assignments)
        if lhs == self.lhs and rhs == self.rhs:
            return self
        else:
            return self.__class__(lhs=lhs, operator=self.operator, rhs=rhs)

    def __str__(self):
        return f"({self.lhs!s} {self.operator.symbol} {self.rhs!s})"


class KnowledgeBase:
    def __init__(self, monkeys: Dict[Union[str, Symbol], Operand]):
        self.expressions: Dict[Symbol, Operand] = {
            Symbol(k): v
            for k, v in monkeys.items()
        }

    def __contains__(self, item: Union[str, Symbol]):
        if isinstance(item, str):
            item = Symbol(item)
        elif not isinstance(item, Symbol):
            return False
        return item in self.expressions

    def __getitem__(self, item: Union[str, Symbol]):
        if isinstance(item, str):
            item = Symbol(item)
        return self.expressions[item]

    def __setitem__(self, key: Union[str, Symbol], value: Operand):
        if isinstance(key, str):
            key = Symbol(key)
        del self[key]
        self.expressions[key] = value

    def __delitem__(self, key: Union[str, Symbol]):
        if isinstance(key, str):
            key = Symbol(key)
        if key in self.expressions:
            del self.expressions[key]

    def resolve(self):
        self.simplify()
        if any(isinstance(e, Expression) for e in self.expressions):
            expressions = (k for k, v in self.expressions.items() if isinstance(v, Expression))
            raise ValueError(f"Could not resolve values for these monkeys: "
                             f"{', '.join(map(str, expressions))}")

    def simplify(self, *expressions: Union[str, Symbol, Expression]) -> List[Operand]:
        if not expressions:
            # update all expressions
            if not self.expressions:
                return []
            return self.simplify(*self.expressions.keys())

        remaining: Set[int] = set(range(len(expressions)))
        done = False
        results: List[Operand] = list(expressions)
        while remaining and not done:
            done = True
            for i, expression in enumerate(results):
                if i not in remaining:
                    continue
                if not isinstance(expression, Expression):
                    expression = self[expression]
                if isinstance(expression, int):
                    results[i] = expression
                    remaining.remove(i)
                    continue
                simplified = expression.simplify(self)
                if simplified != expression:
                    # the value changed
                    done = False
                    original_expression = expressions[i]
                    if not isinstance(original_expression, Expression) and original_expression in self:
                        # update our local value
                        self[original_expression] = simplified
                    results[i] = simplified
                if isinstance(simplified, int):
                    remaining.remove(i)
        return [result for result, original in zip(results, expressions) if result != original]

    @classmethod
    def load(cls, path: Path) -> "KnowledgeBase":
        monkeys: Dict[str, Union[int, Expression]] = {}
        with open(path, "r") as f:
            for line in f:
                name, operands = line.split(": ")
                if name in monkeys:
                    raise ValueError(f"Duplicate monkey definition: {name!r}")
                try:
                    monkeys[name] = int(operands)
                except ValueError:
                    # treat it as a binary operator
                    for oper in Operator:
                        char = f" {oper.symbol} "
                        if char in operands:
                            lhs, rhs = operands.split(char)
                            monkeys[name] = Expression(lhs=Symbol(lhs.strip()), rhs=Symbol(rhs.strip()), operator=oper)
                            break
                    else:
                        raise ValueError(line)
        return KnowledgeBase(monkeys)


@challenge(day=21)
def root_yell(path: Path) -> int:
    kb = KnowledgeBase.load(path)
    return kb.simplify("root")[0]


"""
--- Part Two ---
Due to some kind of monkey-elephant-human mistranslation, you seem to have misunderstood a few key details about the riddle.

First, you got the wrong job for the monkey named root; specifically, you got the wrong math operation. The correct operation for monkey root should be =, which means that it still listens for two numbers (from the same two monkeys as before), but now checks that the two numbers match.

Second, you got the wrong monkey for the job starting with humn:. It isn't a monkey - it's you. Actually, you got the job wrong, too: you need to figure out what number you need to yell so that root's equality check passes. (The number that appears after humn: in your input is now irrelevant.)

In the above example, the number you need to yell to pass root's equality test is 301. (This causes root to get the same number, 150, from both of its monkeys.)

What number do you yell to pass root's equality test?
"""


@challenge(day=21)
def root_equality_test(path: Path) -> int:
    kb = KnowledgeBase.load(path)
    root = kb["root"]
    root = Expression(lhs=root.lhs, rhs=root.rhs, operator=Operator.EQUALS)
    kb["root"] = root
    kb["humn"] = Symbol("humn")
    equation = root.simplify(kb)

