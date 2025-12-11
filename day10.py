import re
import timeit
from collections import defaultdict
from math import dist
import functools
import z3

SAMPLE = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def parse(input):
    machines = [ (int(''.join(reversed(line.split()[0][1:-1].replace('.','0').replace('#','1'))), 2),
                  [sum(2**int(x) for x in t[1:-1].split(',')) for t in line.split()[1:-1]],
                  [int(j) for j in line.split()[-1][1:-1].split(',')]
                 )
                for line in input.splitlines() ]
    return machines


def parse2(input):
    machines = [ ([eval(f"[{t[1:-1]}]") for t in line.split()[1:-1]],
                  [int(j) for j in line.split()[-1][1:-1].split(',')]
                 )
                for line in input.splitlines() ]
    return machines


def part1(input):
    machines = parse(input)
    result = 0
    for target, buttons, costs in machines:
        states = dict()
        edge = { 0 }
        steps = 1
        while edge:
            next_edge = set()
            for state in edge:
                for button in buttons:
                    next_state = state ^ button
                    if next_state not in states:
                        next_edge.add(next_state)
                        states[next_state] = steps
            edge = next_edge
            steps += 1
        result += states[target]

    return result


def part2(input):
    machines = parse2(input)
    result = 0
    for buttons, target in machines:
        equations = [
            (t, [bi for bi, b in enumerate(buttons) if ti in b ])
            for ti, t in enumerate(target)
        ]
        z_buttons = [ z3.Int(f"b{bi}") for bi in range(len(buttons)) ]

        s = z3.Solver()
        for zb in z_buttons:
            s.add(zb >= 0)

        for t,bis in equations:
            s.add(t == sum((z_buttons[bi] for bi in bis[1:]), start=z_buttons[bis[0]]))

        s.push()
        first = True
        while s.check() == z3.sat:
            if not first:
                s.pop()
            model = s.model()
            presses = sum(model[b].py_value() for b in z_buttons)
            s.push()
            s.add(sum(z_buttons[1:], z_buttons[0]) < presses)
            first = False

        result += presses

    return result


def test_part1():
    assert part1(SAMPLE) == 7


def test_part2():
    assert part2(SAMPLE) == 33


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 409

    result = part2(INPUT)
    print("part2:", result)
    assert result == 15489

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
