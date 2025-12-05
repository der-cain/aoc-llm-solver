def parse(input_data):
    # Split into lines
    return [list(line) for line in input_data.strip().split('\n')]

def count_neighbors(grid, r, c, rows, cols):
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] == '@':
                count += 1
    return count

def part1(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    accessible_count = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                neighbors = count_neighbors(grid, r, c, rows, cols)
                if neighbors < 4:
                    accessible_count += 1
    return accessible_count

def part2(grid):
    # Working copy of grid since we modify it
    current_grid = [row[:] for row in grid]
    rows = len(current_grid)
    cols = len(current_grid[0]) if rows > 0 else 0
    
    total_removed = 0
    
    while True:
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if current_grid[r][c] == '@':
                    neighbors = count_neighbors(current_grid, r, c, rows, cols)
                    if neighbors < 4:
                        to_remove.append((r, c))
        
        if not to_remove:
            break
            
        total_removed += len(to_remove)
        for r, c in to_remove:
            current_grid[r][c] = '.' # Or 'x', effectively not '@'
            
    return total_removed
