def parse(data):
    lines = data.splitlines()
    if not lines:
        return []
    
    # Pad lines to max length to form a proper grid
    max_len = max(len(line) for line in lines)
    grid = [line.ljust(max_len) for line in lines]
    
    cols = len(grid[0])
    rows = len(grid)
    
    # Identify empty columns (separators)
    empty_cols = []
    for c in range(cols):
        is_empty = True
        for r in range(rows):
            if grid[r][c] != ' ':
                is_empty = False
                break
        if is_empty:
            empty_cols.append(c)
            
    # Group columns into problems
    problem_ranges = []
    start_col = 0
    # Add a virtual empty column at the end to close the last problem
    for split_col in empty_cols + [cols]:
        if split_col > start_col:
            problem_ranges.append((start_col, split_col))
        start_col = split_col + 1
        
    problems = []
    for start, end in problem_ranges:
        # Extract problem block
        block = []
        for r in range(rows):
            line_slice = grid[r][start:end]
            block.append(line_slice)
        
        if not block:
            continue
            
        # The operator is at the bottom (last row) of the block
        # Find the operator character in the last row
        last_row = block[-1]
        operator = None
        if '+' in last_row:
            operator = '+'
        elif '*' in last_row:
            operator = '*'
            
        if operator:
             problems.append((operator, block))
        
    return problems

def part1(parsed_data):
    total = 0
    for operator, block in parsed_data:
        # Part 1: Numbers are horizontal sequences
        # We process all rows except the last one (which has the operator)
        numbers = []
        for line in block[:-1]:
            # Digits are sequences of characters separated by spaces
            # Since strip() removes leading/trailing spaces, and split() handles internal spaces
            parts = line.split()
            for p in parts:
                try:
                    numbers.append(int(p))
                except ValueError:
                    pass
                    
        if not numbers:
            continue
            
        if operator == '+':
            total += sum(numbers)
        elif operator == '*':
            res = 1
            for n in numbers:
                res *= n
            total += res
            
    return total

def part2(parsed_data):
    total = 0
    for operator, block in parsed_data:
        # Part 2: Numbers are vertical columns, read Right-to-Left
        # Block has rows. We need to iterate columns of the block.
        # block[r][c] is character at row r, col c within the block.
        
        rows = len(block)
        cols = len(block[0])
        
        numbers = []
        
        # Iterate cols from Right to Left
        for c in range(cols - 1, -1, -1):
            # Extract digits from Top to Bottom (excluding last row with operator)
            digits = ""
            for r in range(rows - 1):
                char = block[r][c]
                if char.isdigit():
                    digits += char
            
            if digits:
                numbers.append(int(digits))
                
        if not numbers:
            continue
            
        if operator == '+':
            total += sum(numbers)
        elif operator == '*':
            res = 1
            for n in numbers:
                res *= n
            total += res
            
    return total
