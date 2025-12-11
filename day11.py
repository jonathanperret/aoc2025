import re
import timeit
from collections import defaultdict
import networkx as nx
from more_itertools import ilen

SAMPLE = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

SAMPLE2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

SAMPLE3 = """svr: aaa bbb
aaa: dac
dac: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: fft
fft: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def parse(input):
    return [ (line.split()[0][:-1], line.split()[1:])
             for line in input.splitlines() ]


def part1(input):
    devices = parse(input)
    G = nx.DiGraph([(src,dst) for src, dsts in devices
                    for dst in dsts])
    result = ilen(nx.all_simple_paths(G, 'you', 'out'))
    (nx.all_simple_paths(G, 'you', 'out'))
    return result


def count_paths(G, src, dst):
    Gr = nx.reverse_view(G)
    counts = defaultdict(int, { dst: 1 })
    for n in nx.topological_sort(Gr):
        if n == src:
            break
        for parent in Gr[n]:
            counts[parent] += counts[n]

    return counts[src]


def part2(input):
    devices = parse(input)
    G = nx.DiGraph([(src,dst) for src, dsts in devices
                    for dst in dsts])

    if 'dac' in nx.descendants(G, 'fft'):
        svr_to_fft = count_paths(G, 'svr', 'fft')
        fft_to_dac = count_paths(G, 'fft', 'dac')
        dac_to_out = count_paths(G, 'dac', 'out')

        return svr_to_fft * fft_to_dac * dac_to_out
    else:
        svr_to_dac = count_paths(G, 'svr', 'dac')
        dac_to_fft = count_paths(G, 'dac', 'fft')
        fft_to_out = count_paths(G, 'fft', 'out')

        return svr_to_dac * dac_to_fft * fft_to_out


def test_part1():
    assert part1(SAMPLE) == 5


def test_part2():
    assert part2(SAMPLE2) == 2


def test_part2_flipped():
    assert part2(SAMPLE3) == 2


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 613

    result = part2(INPUT)
    print("part2:", result)
    assert result == 372918445876116

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
