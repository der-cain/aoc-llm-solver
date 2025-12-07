import heapq

def parse(data):
    grid = []
    for line in data.splitlines():
        if not line.strip():
            continue
        grid.append([int(c) for c in line.strip()])
    return grid

def solve(grid):
    rows = len(grid)
    cols = len(grid[0])
    target = (rows - 1, cols - 1)
    
    # Dijkstra
    # (cost, r, c)
    pq = [(0, 0, 0)]
    visited = set()
    min_costs = {(0, 0): 0}
    
    while pq:
        cost, r, c = heapq.heappop(pq)
        
        if (r, c) == target:
            return cost
            
        if (r, c) in visited:
            continue
        visited.add((r, c))
        
        # Optimization: repeated visits check
        if cost > min_costs.get((r, c), float('inf')):
            continue
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + grid[nr][nc]
                if new_cost < min_costs.get((nr, nc), float('inf')):
                    min_costs[(nr, nc)] = new_cost
                    heapq.heappush(pq, (new_cost, nr, nc))
                    
    return -1

def part1(parsed_data):
    return solve(parsed_data)

def expand_grid(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    new_rows = rows * 5
    new_cols = cols * 5
    
    new_grid = [[0] * new_cols for _ in range(new_rows)]
    
    for r in range(new_rows):
        for c in range(new_cols):
            # Original coordinates
            or_r = r % rows
            or_c = c % cols
            
            # Tile offset
            tr = r // rows
            tc = c // cols
            
            # New value: original + distance (tr + tc)
            val = grid[or_r][or_c] + tr + tc
            
            # Wrap 9 -> 1
            # Formula: (val - 1) % 9 + 1
            val = (val - 1) % 9 + 1
            
            new_grid[r][c] = val
            
    return new_grid

def part2(parsed_data):
    expanded = expand_grid(parsed_data)
    return solve(expanded)
