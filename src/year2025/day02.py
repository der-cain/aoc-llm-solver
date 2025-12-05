def parse(input_data):
    # Input is comma separated ranges, e.g. "11-22,95-115"
    # Can ideally handle multiline if wrapped, or single line.
    input_data = input_data.replace('\n', '').strip()
    parts = input_data.split(',')
    ranges = []
    for part in parts:
        if not part.strip():
            continue
        start_str, end_str = part.split('-')
        ranges.append((int(start_str), int(end_str)))
    return ranges

def is_invalid_id(num):
    s = str(num)
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]

def part1(data):
    total_invalid_sum = 0
    for start, end in data:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total_invalid_sum += num
    return total_invalid_sum

def is_part2_invalid(num):
    s = str(num)
    n = len(s)
    # Check all possible lengths for the repeating unit substring 'p'
    # Length of p (d) must be a divisor of n, and d < n (so it repeats at least twice)
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            subtree = s[:d]
            repeats = n // d
            if subtree * repeats == s:
                return True
    return False

def part2(data):
    total_invalid_sum = 0
    for start, end in data:
        for num in range(start, end + 1):
            if is_part2_invalid(num):
                total_invalid_sum += num
    return total_invalid_sum
