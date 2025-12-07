def parse(data):
    grid = []
    for line in data.splitlines():
        if not line.strip():
            continue
        grid.append([int(c) for c in line.strip()])
    return grid

def step(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    # Increase energy by 1
    flashed = set()
    queue = []
    
    for r in range(rows):
        for c in range(cols):
            grid[r][c] += 1
            if grid[r][c] > 9:
                queue.append((r, c))
                flashed.add((r, c))
                
    # Process flashes
    idx = 0
    while idx < len(queue):
        r, c = queue[idx]
        idx += 1
        
        # Neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    grid[nr][nc] += 1
                    if grid[nr][nc] > 9 and (nr, nc) not in flashed:
                        flashed.add((nr, nc))
                        queue.append((nr, nc))
                        
    # Reset energy to 0 for flashed
    for r, c in flashed:
        grid[r][c] = 0
        
    return len(flashed)

def part1(parsed_data):
    # Need deepcopy or similar if we modify grid in place?
    # Usually safer.
    grid = [row[:] for row in parsed_data]
    
    total_flashes = 0
    for _ in range(100):
        total_flashes += step(grid)
        
    return total_flashes

def part2(parsed_data):
    # Need deepcopy or similar
    grid = [row[:] for row in parsed_data]
    
    rows = len(grid)
    cols = len(grid[0])
    total_octopuses = rows * cols
    
    step_count = 0
    while True:
        step_count += 1
        flashes = step(grid)
        if flashes == total_octopuses:
            return step_count
