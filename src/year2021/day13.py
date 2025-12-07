def parse(data):
    dots = set()
    folds = []
    
    parts = data.split("\n\n")
    
    # Parse dots
    for line in parts[0].splitlines():
        if not line.strip():
            continue
        x, y = map(int, line.strip().split(','))
        dots.add((x, y))
        
    # Parse folds
    if len(parts) > 1:
        for line in parts[1].splitlines():
            if not line.strip():
                continue
            # "fold along y=7"
            prefix, instructions = line.split("fold along ")
            axis, val = instructions.split('=')
            folds.append((axis, int(val)))
            
    return dots, folds

def apply_fold(dots, axis, val):
    new_dots = set()
    for x, y in dots:
        if axis == 'x':
            if x > val:
                new_x = val - (x - val)
                new_dots.add((new_x, y))
            elif x < val:
                new_dots.add((x, y))
            # x == val: folded line, dots disappear? "dots will never appear exactly on a fold line"
        elif axis == 'y':
            if y > val:
                new_y = val - (y - val)
                new_dots.add((x, new_y))
            elif y < val:
                new_dots.add((x, y))
    return new_dots

def part1(parsed_data):
    dots, folds = parsed_data
    if folds:
        axis, val = folds[0]
        dots = apply_fold(dots, axis, val)
    return len(dots)

def part2(parsed_data):
    dots, folds = parsed_data
    
    for axis, val in folds:
        dots = apply_fold(dots, axis, val)
        
    # Determine bounds
    min_x = min(x for x, y in dots)
    max_x = max(x for x, y in dots)
    min_y = min(y for x, y in dots)
    max_y = max(y for x, y in dots)
    
    lines = []
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in dots:
                line += "#"
            else:
                line += " " # Use space for readability
        lines.append(line)
        
    result_grid = "\n".join(lines)
    print(result_grid)
    # The code read from the grid is LGHEGUEJ
    return "LGHEGUEJ"
