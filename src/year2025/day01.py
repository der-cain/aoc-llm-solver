def parse(input_data):
    # Split by any whitespace to handle both single-line and multi-line inputs
    return input_data.strip().split()

def part1(data):
    current = 50
    count_zero = 0
    
    for instruction in data:
        direction = instruction[0]
        amount = int(instruction[1:])
        
        if direction == 'L':
            # Left: towards lower numbers
            current = (current - amount) % 100
        elif direction == 'R':
            # Right: towards higher numbers
            current = (current + amount) % 100
            
        if current == 0:
            count_zero += 1
            
    return count_zero

def part2(data):
    return "Not implemented"
