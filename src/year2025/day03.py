def parse(input_data):
    # Split into lines
    return input_data.strip().split()

def solve_line(line):
    max_val = 0
    # Try all pairs of indices (i, j) with i < j
    # This is O(N^2), suitable for typical AoC line lengths.
    for i in range(len(line)):
        for j in range(i + 1, len(line)):
            val = int(line[i] + line[j])
            if val > max_val:
                max_val = val
    return max_val

def part1(data):
    total = 0
    for line in data:
        line = line.strip()
        if not line:
            continue
        total += solve_line(line)
    return total

def part2(data):
    return "Not implemented"
