import re
import timeit
from collections import defaultdict
from math import dist

SAMPLE = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def parse(input):
    tiles = [ list(map(int,line.split(','))) for line in input.splitlines() ]
    return tiles


def area(tile1, tile2):
    return (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)


def part1(input, limit=1000):
    tiles = parse(input)
    areas = [ area(tile1, tile2)
              for i1, tile1 in enumerate(tiles)
              for tile2 in tiles[:i1] ]
    return max(areas)


def check(tiles, tile1, tile2):
    minx, maxx = min(tile1[0], tile2[0]), max(tile1[0], tile2[0])
    miny, maxy = min(tile1[1], tile2[1]), max(tile1[1], tile2[1])
    pos1 = tiles[-1]
    for pos2 in tiles:
        if not(
                (pos1[0] <= minx and pos2[0] <= minx) or
                (pos1[0] >= maxx and pos2[0] >= maxx) or
                (pos1[1] <= miny and pos2[1] <= miny) or
                (pos1[1] >= maxy and pos2[1] >= maxy) ):
            return False
        pos1 = pos2

    return True


def part2(input, write=False):
    tiles = parse(input)
    areas = [ area(tile1, tile2)
              for i1, tile1 in enumerate(tiles)
              for tile2 in tiles[:i1]
              if check(tiles, tile1, tile2) ]
    return max(areas)


def test_part1():
    assert part1(SAMPLE) == 50


def test_part2():
    assert part2(SAMPLE) == 24


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 4743645488

    result = part2(INPUT, write=True)
    print("part2:", result)
    assert result == 1529011204

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
