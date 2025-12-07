from collections import Counter

def parse(data):
    parts = data.split("\n\n")
    template = parts[0].strip()
    rules = {}
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        pair, insert = line.strip().split(" -> ")
        rules[pair] = insert
    return template, rules

def solve(parsed_data, steps):
    template, rules = parsed_data
    
    # Initial pair counts
    pairs = Counter()
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pairs[pair] += 1
        
    # Initial element counts
    elements = Counter(template)
    
    for _ in range(steps):
        new_pairs = Counter()
        for pair, count in pairs.items():
            if pair in rules:
                insert = rules[pair]
                # pair AB -> C becomes AC and CB
                new_pairs[pair[0] + insert] += count
                new_pairs[insert + pair[1]] += count
                # Element C is added count times
                elements[insert] += count
            else:
                new_pairs[pair] += count
        pairs = new_pairs
        
    # Calculate score
    counts = elements.values()
    return max(counts) - min(counts)

def part1(parsed_data):
    return solve(parsed_data, 10)

def part2(parsed_data):
    return solve(parsed_data, 40)
