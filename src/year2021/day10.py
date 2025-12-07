def parse(data):
    lines = []
    for line in data.splitlines():
        if not line.strip():
            continue
        lines.append(line.strip())
    return lines

def part1(data):
    total_score = 0
    
    # Points for illegal characters
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    
    # Matching pairs
    pairs = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    
    for line in data:
        stack = []
        for char in line:
            if char in pairs:
                stack.append(char)
            else:
                # Closing character
                if not stack:
                    # Incomplete or invalid? Problem says find first illegal character.
                    # If stack empty but closing char found, it's illegal.
                    total_score += points[char]
                    break
                
                last_open = stack.pop()
                if pairs[last_open] != char:
                    # Mismatch -> Corrupted
                    total_score += points[char]
                    break
                    
    return total_score

def part2(data):
    scores = []
    
    # Points for completion characters
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    
    # Matching pairs
    pairs = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    
    for line in data:
        stack = []
        corrupted = False
        for char in line:
            if char in pairs:
                stack.append(char)
            else:
                if not stack:
                    corrupted = True
                    break
                last_open = stack.pop()
                if pairs[last_open] != char:
                    corrupted = True
                    break
        
        if not corrupted:
            # Incomplete line, calculate score
            score = 0
            # Complete the line by popping from stack
            while stack:
                last_open = stack.pop()
                closing_char = pairs[last_open]
                score = score * 5 + points[closing_char]
            scores.append(score)
            
    scores.sort()
    return scores[len(scores) // 2]
