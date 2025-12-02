from more_itertools import *

SAMPLE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

def parse(input):
    lines = input.splitlines()
    values = [(-1 if line[0] == "L" else 1) * int(line[1:]) for line in lines]
    return values

def part1(input):
    values = parse(input)
    matches = 0
    position = 50
    for value in values:
        position = (position + value) % 100
        if position == 0:
            matches += 1
    return matches

def part2(input):
    values = parse(input)
    matches = 0
    position = 50
    for value in values:
        matches += abs(value) // 100
        incr = (1 if value > 0 else -1)
        value = abs(value) % 100 * incr
        while abs(value) > 0:
            position = (position + incr) % 100
            if position == 0:
                matches += 1
            value = value - incr
    return matches

INPUT = open("day1.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
