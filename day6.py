import re
import timeit
from functools import reduce
from more_itertools import transpose
from operator import add, mul

SAMPLE = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

def parse(input):
    grid = [ line.split() for line in input.splitlines() ]
    return transpose(grid)


def part1(input):
    problems = parse(input)
    results = []
    for p in problems:
        op = p[-1]
        result = 1 if op == '*' else 0
        for n in p[:-1]:
            if op == '*':
                result *= int(n)
            else:
                result += int(n)
        results.append(result)
    return sum(results)


def part2(input):
    grid = list(transpose(input.splitlines()))
    results = []
    result = 0
    op = '+'
    for column in grid:
        if all(c == " " for c in column):
            results.append(result)
            continue
        if column[-1] == '*':
            result = 1
            op = mul
        elif column[-1] == '+':
            result = 0
            op = add
        num = int(''.join(column[:-1]))
        result = op(result, num)
    results.append(result)
    return sum(results)


def test_part1():
    assert part1(SAMPLE) == 4277556


def test_part2():
    assert part2(SAMPLE) == 3263827


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 5227286044585

    result = part2(INPUT)
    print("part2:", result)
    assert result == 10227753257799

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
