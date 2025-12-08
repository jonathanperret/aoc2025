import re
import timeit
from collections import defaultdict
from math import dist

SAMPLE = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

def parse(input):
    boxes = [ list(map(int,line.split(','))) for line in input.splitlines() ]
    return boxes


def merge_shortest(boxes, limit=None):
    shortest = sorted(((i1, i2)
                        for i1 in range(len(boxes))
                        for i2 in range(i1)),
                       key=lambda pair: dist(boxes[pair[0]], boxes[pair[1]]))
    circuits = { i: { i } for i in range(len(boxes)) }
    parents = list(range(len(boxes)))
    for i1, i2 in shortest[:limit]:
        circuit1, circuit2 = parents[i1], parents[i2]
        if circuit1 != circuit2:
            for i in circuits[circuit2]:
                parents[i] = circuit1
            circuits[circuit1].update(circuits[circuit2])
            del circuits[circuit2]
            if len(circuits) == 1:
                return (i1, i2)
    return circuits


def part1(input, limit=1000):
    boxes = parse(input)
    circuits = merge_shortest(boxes, limit)
    sizes = list(reversed(sorted(len(circuit) for circuit in circuits.values())))
    return sizes[0] * sizes[1] * sizes[2]


def part2(input):
    boxes = parse(input)
    last1, last2 = merge_shortest(boxes)
    return boxes[last1][0] * boxes[last2][0]


def test_part1():
    assert part1(SAMPLE, 10) == 40


def test_part2():
    assert part2(SAMPLE) == 25272


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 103488

    result = part2(INPUT)
    print("part2:", result)
    assert result == 8759985540

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
