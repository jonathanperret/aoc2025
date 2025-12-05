import re
import timeit

SAMPLE = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

def parse(input):
    ranges, ingredients = input.split("\n\n")
    ranges = [ tuple(map(int, line.split("-"))) for line in ranges.splitlines() ]
    ingredients = list(map(int, ingredients.splitlines()))
    return ranges, ingredients


def part1(input):
    ranges, ingredients = parse(input)
    fresh = sum(
      any(
        ingredient >= range[0] and ingredient <= range[1] for range in ranges
      )
      for ingredient in ingredients
    )
    return fresh

from functools import reduce
from more_itertools import partition
def part2(input):
    ranges, _ = parse(input)
    merged = []
    for new_range in ranges:
        non_intersecting, intersecting = \
            partition(lambda r: new_range[0] <= r[1] and new_range[1] >= r[0],
                      merged)
        union = reduce(lambda r1, r2: (
                    min(r1[0], r2[0]),
                    max(r1[1], r2[1]),
                ), intersecting, new_range)
        merged = list(non_intersecting) + [ union ]
    result = sum(b - a + 1 for (a, b) in merged)
    return result


def test_part1():
    assert part1(SAMPLE) == 3


def test_part2():
    assert part2(SAMPLE) == 14


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 773

    result = part2(INPUT)
    print("part2:", result)
    assert result == 332067203034711
#
#    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
#    print("time=", total / num)
