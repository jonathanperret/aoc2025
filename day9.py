import re
import timeit
from collections import defaultdict
from math import dist
from bisect import bisect_left, bisect_right
from itertools import islice

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


def check(h_edges, v_edges, tile1, tile2):
    minx, maxx = sorted((tile1[0], tile2[0]))
    miny, maxy = sorted((tile1[1], tile2[1]))

    h_first = bisect_right(h_edges, miny, key=lambda e:e[0])
    h_last = bisect_left(h_edges, maxy, key=lambda e:e[0])

    for h_edge, x1, x2 in islice(h_edges, h_first, h_last):
        if ((x1 > minx or x2 > minx) and
            (x1 < maxx or x2 < maxx)):
            return False

    v_first = bisect_right(v_edges, minx, key=lambda e:e[0])
    v_last = bisect_left(v_edges, maxx, key=lambda e:e[0])

    for v_edge, y1, y2 in islice(v_edges, v_first, v_last):
        if ( (y1 <= miny and y2 <= miny) or
             (y1 >= maxy and y2 >= maxy) ):
            continue
        return False

    return True


def part2(input, write=False):
    tiles = parse(input)
    edges = [ (tile1, tiles[(i1 + 1) % len(tiles)])
              for i1, tile1 in enumerate(tiles) ]
    h_edges = sorted(
                (tile1[1], *sorted((tile1[0], tile2[0])))
                for (tile1, tile2) in edges
                if tile1[1] == tile2[1]
              )
    v_edges = sorted(
                (tile1[0], *sorted((tile1[1], tile2[1])))
                for (tile1, tile2) in edges
                if tile1[0] == tile2[0]
              )
    areas = [ area(tile1, tile2)
              for i1, tile1 in enumerate(tiles)
              for tile2 in tiles[:i1]
              if check(h_edges, v_edges, tile1, tile2) ]
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
