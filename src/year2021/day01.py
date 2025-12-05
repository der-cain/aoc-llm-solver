def parse(data):
    return [int(line) for line in data.splitlines() if line.strip()]

def part1(data):
    count = 0
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            count += 1
    return count

def part2(data):
    count = 0
    # Sliding window of size 3
    # Compare sum(data[i:i+3]) with sum(data[i-1:i+2])
    # Which simplifies to comparing data[i+2] > data[i-1] because the middle two elements are shared.
    
    # Or just implementing straightforwardly:
    for i in range(1, len(data) - 2):
        window_a = data[i-1] + data[i] + data[i+1]
        window_b = data[i] + data[i+1] + data[i+2]
        
        if window_b > window_a:
            count += 1
            
    return count
