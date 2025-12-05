def parse(input_data):
    # expect two sections separated by blank line
    parts = input_data.strip().split('\n\n')
    if len(parts) < 2:
        # Fallback if weird formatting - maybe single line?
        # But description says "blank line".
        # Let's try to assume first line is ranges if only 1 part? 
        # But ranges and IDs look different.
        # Actually, let's stick to split by \n\n.
        # If the user copy-pastes example which might lack newlines, it might be tricky.
        # But let's assume valid input contains blank line.
        # However, looking at the example text "3-5 10-14 ... 1 5 8 ...", it might be on one line? 
        # "consists of ... ranges, a blank line, and ... IDs".
        pass
    
    range_section = parts[0]
    id_section = parts[1]
    
    ranges = []
    # Parse ranges. Might be space or newline separated?
    for token in range_section.split():
        if '-' in token:
            s, e = token.split('-')
            ranges.append((int(s), int(e)))
            
    ids = []
    for token in id_section.split():
        ids.append(int(token))
        
    return ranges, ids

def part1(parsed_data):
    ranges, ids = parsed_data
    count = 0
    for id_val in ids:
        is_fresh = False
        for start, end in ranges:
            if start <= id_val <= end:
                is_fresh = True
                break
        if is_fresh:
            count += 1
    return count

def part2(data):
    return "Not implemented"
