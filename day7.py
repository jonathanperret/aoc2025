import re
import timeit
from collections import defaultdict

SAMPLE = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

def parse(input):
    grid = input.splitlines()
    return grid


def part1(input):
    grid = parse(input)
    tachyons = { grid[0].index('S') }
    splits = 0
    for row in grid[1:]:
        new_tachyons = set()
        for col in tachyons:
            if row[col] == '^':
                splits += 1
                if col > 0:
                    new_tachyons.add(col - 1)
                if col < len(row)-1:
                    new_tachyons.add(col + 1)
            else:
                new_tachyons.add(col)
        tachyons = new_tachyons
    return splits


def part2(input):
    grid = parse(input)
    tachyons = { grid[0].index('S'): 1 }
    for row in grid[1:]:
        new_tachyons = defaultdict(int)
        for col, count in tachyons.items():
            if row[col] == '^':
                if col > 0:
                    new_tachyons[col - 1] += count
                if col < len(row)-1:
                    new_tachyons[col + 1] += count
            else:
                new_tachyons[col] += count
        tachyons = new_tachyons
    return sum(tachyons.values())


def test_part1():
    assert part1(SAMPLE) == 21


def test_part2():
    assert part2(SAMPLE) == 40


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1667

    result = part2(INPUT)
    print("part2:", result)
    assert result == 62943905501815

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
