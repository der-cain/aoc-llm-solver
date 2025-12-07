def parse(data):
    line = data.strip()
    if not line:
        return []
    return list(map(int, line.split(',')))

def part1(data):
    if not data:
        return 0
    
    # Sort data to find median
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = sorted_data[n // 2]
    
    fuel = sum(abs(x - median) for x in data)
    return fuel

def part2(data):
    if not data:
        return 0
        
    # For part 2, fuel cost is triangular number: n*(n+1)/2
    # The optimal position is near the mean.
    
    mean = sum(data) / len(data)
    possible_targets = [int(mean), int(mean) + 1]
    
    min_fuel = float('inf')
    
    for target in possible_targets:
        current_fuel = 0
        for x in data:
            diff = abs(x - target)
            cost = (diff * (diff + 1)) // 2
            current_fuel += cost
        min_fuel = min(min_fuel, current_fuel)
        
    return min_fuel
