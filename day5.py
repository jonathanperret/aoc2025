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


def part2(input):
    ranges, _ = parse(input)
    ranges.sort()
    last_counted = -1
    result = 0
    for r in ranges:
        if r[1] > last_counted:
            result += r[1] - last_counted
            if r[0] > last_counted + 1:
                result -= r[0] - last_counted -1
            last_counted = r[1]
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

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
