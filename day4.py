import re
import timeit
from more_itertools import convolve, transpose

SAMPLE = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

def parse(input):
    return [ [ 1 if c == '@' else 0 for c in line ] for line in input.splitlines() ]


def count_neighbors(grid, i, j):
    height = len(grid)
    width = len(grid[0])
    neighbors = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            if i + di >= width or i + di < 0:
                continue
            if j + dj >= height or j + dj < 0:
                continue
            neighbors += grid[i + di][j + dj]
    return neighbors


def display(grid):
    print("\n".join("".join("@" if c == 1 else "." for c in line) for line in grid))
    print("")


def part1(input):
    grid = parse(input)
    # display(grid)
    height = len(grid)
    width = len(grid[0])
    rolls = 0
    counts = [ [ count_neighbors(grid, i, j) for j in range(width) ] for i in range(height) ]
    for i in range(height):
        for j in range(width):
            neighbors = counts[i][j]
            if grid[i][j] == 1 and neighbors < 4:
                rolls += 1
    return rolls


def part2(input):
    grid = parse(input)
    height = len(grid)
    width = len(grid[0])
    # display(grid)
    new_grid = [ line[:] for line in grid ]
    rolls = 0
    while True:
        found = False
        for i in range(height):
            for j in range(width):
                neighbors = count_neighbors(grid, i, j)
                if grid[i][j] == 1 and neighbors < 4:
                    found = True
                    rolls += 1
                    new_grid[i][j] = 0
        # display(new_grid)
        grid = new_grid
        if not found:
            break
    return rolls


def test_part1():
    assert part1(SAMPLE) == 13


def test_part2():
    assert part2(SAMPLE) == 43


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1480

    result = part2(INPUT)
    print("part2:", result)
    assert result == 8899

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
