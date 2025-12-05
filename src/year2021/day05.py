from collections import defaultdict

def parse(data):
    lines = []
    for line in data.splitlines():
        if not line.strip():
            continue
        parts = line.split(' -> ')
        p1 = list(map(int, parts[0].split(',')))
        p2 = list(map(int, parts[1].split(',')))
        lines.append((p1, p2))
    return lines

def solve(data, include_diagonals=False):
    grid = defaultdict(int)
    
    for (x1, y1), (x2, y2) in data:
        is_diag = (x1 != x2) and (y1 != y2)
        
        if is_diag and not include_diagonals:
            continue
            
        dx = 0
        if x2 > x1: dx = 1
        elif x2 < x1: dx = -1
        
        dy = 0
        if y2 > y1: dy = 1
        elif y2 < y1: dy = -1
        
        curr_x, curr_y = x1, y1
        while True:
            grid[(curr_x, curr_y)] += 1
            if curr_x == x2 and curr_y == y2:
                break
            curr_x += dx
            curr_y += dy
            
    count = sum(1 for v in grid.values() if v >= 2)
    return count

def part1(data):
    return solve(data, include_diagonals=False)

def part2(data):
    return solve(data, include_diagonals=True)
