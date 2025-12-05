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

def part2(data):
    return "Not implemented"
