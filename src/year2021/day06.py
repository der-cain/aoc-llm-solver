from collections import Counter, defaultdict

def parse(data):
    # Data is a single line of comma-separated integers
    line = data.strip()
    if not line:
        return []
    return list(map(int, line.split(',')))

def solve(fish, days):
    counts = Counter(fish)
    
    for _ in range(days):
        new_counts = defaultdict(int)
        for timer, count in counts.items():
            if timer == 0:
                new_counts[6] += count
                new_counts[8] += count
            else:
                new_counts[timer - 1] += count
        counts = new_counts
        
    return sum(counts.values())

def part1(data):
    return solve(data, 80)

def part2(data):
    return solve(data, 256)
