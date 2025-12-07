import itertools

def parse(data):
    return [int(x) for x in data.splitlines()]

def part1(data):
    return sum(data)

def part2(data):
    current_frequency = 0
    seen_frequencies = {0}
    for change in itertools.cycle(data):
        current_frequency += change
        if current_frequency in seen_frequencies:
            return current_frequency
        seen_frequencies.add(current_frequency)
