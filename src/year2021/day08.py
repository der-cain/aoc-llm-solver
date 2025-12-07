def parse(data):
    lines = []
    for line in data.splitlines():
        if not line.strip():
            continue
        parts = line.split('|')
        patterns = parts[0].strip().split()
        output = parts[1].strip().split()
        lines.append((patterns, output))
    return lines

def part1(data):
    count = 0
    # Segments count:
    # 1: 2
    # 4: 4
    # 7: 3
    # 8: 7
    unique_lengths = {2, 4, 3, 7}
    
    for _, output in data:
        for digit in output:
            if len(digit) in unique_lengths:
                count += 1
                
    return count

def part2(data):
    total = 0
    
    for patterns, output in data:
        # Convert patterns to sets for easier comparison
        patterns = [set(p) for p in patterns]
        
        # Mapping from digit value to pattern set
        digits = {}
        
        # Find unique length digits first
        digits[1] = next(p for p in patterns if len(p) == 2)
        digits[4] = next(p for p in patterns if len(p) == 4)
        digits[7] = next(p for p in patterns if len(p) == 3)
        digits[8] = next(p for p in patterns if len(p) == 7)
        
        # Identify 6-segment digits: 0, 6, 9
        six_segments = [p for p in patterns if len(p) == 6]
        
        # 9 contains 4 as subset
        digits[9] = next(p for p in six_segments if digits[4].issubset(p))
        six_segments.remove(digits[9])
        
        # 0 contains 1 as subset (remaining from 0, 6)
        digits[0] = next(p for p in six_segments if digits[1].issubset(p))
        six_segments.remove(digits[0])
        
        # Remaining is 6
        digits[6] = six_segments[0]
        
        # Identify 5-segment digits: 2, 3, 5
        five_segments = [p for p in patterns if len(p) == 5]
        
        # 3 contains 1 as subset
        digits[3] = next(p for p in five_segments if digits[1].issubset(p))
        five_segments.remove(digits[3])
        
        # 6 contains 5 as subset (remaining from 2, 5)
        digits[5] = next(p for p in five_segments if p.issubset(digits[6]))
        five_segments.remove(digits[5])
        
        # Remaining is 2
        digits[2] = five_segments[0]
        
        # Create reverse mapping for lookup (frozenset to be hashable)
        pattern_map = {frozenset(v): k for k, v in digits.items()}
        
        # Decode output
        decoded_val = 0
        for out in output:
            digit_val = pattern_map[frozenset(out)]
            decoded_val = decoded_val * 10 + digit_val
            
        total += decoded_val
        
    return total
