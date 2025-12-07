import string

def parse(data):
    return data.strip()

def react(polymer):
    stack = []
    for char in polymer:
        if stack and char != stack[-1] and char.lower() == stack[-1].lower():
            stack.pop()
        else:
            stack.append(char)
    return len(stack)

def part1(data):
    return react(data)

def part2(data):
    min_length = float('inf')
    for unit_type in string.ascii_lowercase:
        # Create a new polymer by removing all instances of the current unit type (both lower and upper case)
        temp_polymer = data.replace(unit_type, '').replace(unit_type.upper(), '')
        length = react(temp_polymer)
        if length < min_length:
            min_length = length
    return min_length
