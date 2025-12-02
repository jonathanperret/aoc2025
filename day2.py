from more_itertools import *

SAMPLE = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

def parse(input):
    ranges = input.split(",")
    values = [[int(value) for value in range.split("-")] for range in ranges]
    return values

def part1(input):
    ranges = parse(input)
    ids = [str(id) for r in ranges for id in range(r[0], r[1]+1)]
    invalids = (id for id in ids
                if len(id)%2 == 0 and id[:len(id)//2] == id[len(id)//2:])
    return sum(int(id) for id in invalids)

def part2(input):
    ranges = parse(input)
    result = 0
    for r in ranges:
        for id in range(r[0], r[1]+1):
            s = str(id)
            for l in range(1, len(s)):
                if len(s)%l == 0:
                    if s[:l] * (len(s)//l) == s:
                        result += id
                        break
    return result

INPUT = open("day2.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
