from more_itertools import *

SAMPLE = """987654321111111
811111111111119
234234234234278
818181911112111"""

def parse(input):
    banks = input.splitlines()
    return banks


def find_max_joltage(bank, count):
    if count == 1:
        return max(bank)

    max_battery_value = max(bank[:-(count - 1)])
    max_battery_pos = bank.find(max_battery_value)
    rest = bank[max_battery_pos + 1:]
    return max_battery_value + find_max_joltage(rest, count - 1)


def part1(input):
    banks = parse(input)
    return sum(int(find_max_joltage(bank, 2)) for bank in banks)


def part2(input):
    banks = parse(input)
    return sum(int(find_max_joltage(bank, 12)) for bank in banks)


INPUT = open("day3.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
