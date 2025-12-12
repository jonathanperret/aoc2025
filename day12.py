import re
import timeit
from collections import defaultdict
from more_itertools import ilen

SAMPLE = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

def parse(input):
    blocks = input.split("\n\n")
    shapes = [ block.splitlines()[1:] for block in blocks[:-1] ]
    regions = []
    for line in blocks[-1].splitlines():
        words = line.split()
        regions.append((tuple(int(x) for x in words[0][:-1].split("x")),
                       [int(w) for w in words[1:]]))
    return shapes, regions


def part1(input):
    shapes, regions = parse(input)
    print(shapes)
    areas = [ ilen(c for row in shape for c in row if c=="#")
              for shape in shapes ]
    print(areas)
    ok = 0
    for (w,h),ss in regions:
        r_area = w * h
        area_req = sum(areas[si]*sc for si,sc in enumerate(ss))
        r_area_mod3 = (w - w%3) * (h - h%3)
        if area_req > r_area:
            print("too many tiles needed")
            continue
        if area_req > r_area_mod3:
            print("can't fit in mod3 area")
            return
        area_req_nofit = 9 * sum(ss)
        if area_req_nofit > r_area_mod3:
            print("can't fit in mod3 area with no overlap")
            return

        print(w,h,r_area,area_req, r_area - area_req, r_area_mod3, r_area_mod3 - area_req)
        ok += 1

    return ok


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 497
