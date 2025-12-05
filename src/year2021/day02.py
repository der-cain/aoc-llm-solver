def parse(data):
    result = []
    for line in data.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        result.append((parts[0], int(parts[1])))
    return result

def part1(data):
    horizontal = 0
    depth = 0
    
    for command, val in data:
        if command == "forward":
            horizontal += val
        elif command == "down":
            depth += val
        elif command == "up":
            depth -= val
            
    return horizontal * depth

def part2(data):
    horizontal = 0
    depth = 0
    aim = 0
    
    for command, val in data:
        if command == "forward":
            horizontal += val
            depth += aim * val
        elif command == "down":
            aim += val
        elif command == "up":
            aim -= val
            
    return horizontal * depth
