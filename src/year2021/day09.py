def parse(data):
    grid = []
    for line in data.splitlines():
        if not line.strip():
            continue
        grid.append([int(c) for c in line.strip()])
    return grid

def part1(data):
    rows = len(data)
    cols = len(data[0])
    total_risk = 0
    
    for r in range(rows):
        for c in range(cols):
            height = data[r][c]
            is_low = True
            
            # Check neighbors
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if data[nr][nc] <= height:
                        is_low = False
                        break
            
            if is_low:
                total_risk += 1 + height
                
    return total_risk

def bfs_basin(data, r, c, visited):
    rows = len(data)
    cols = len(data[0])
    queue = [(r, c)]
    size = 0
    visited.add((r, c))
    
    while queue:
        curr_r, curr_c = queue.pop(0)
        size += 1
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in visited and data[nr][nc] != 9:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    return size

def part2(data):
    # Find low points, then BFS for basins
    rows = len(data)
    cols = len(data[0])
    basin_sizes = []
    visited = set()
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited or data[r][c] == 9:
                continue
                
            # It's part of a basin (start of a new one, does not strictly need to be a low point if we scan all)
            # Actually, per problem: "Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin."
            # So just valid points (!= 9) form basins. BFS connected components of != 9.
            size = bfs_basin(data, r, c, visited)
            if size > 0:
                basin_sizes.append(size)
                
    basin_sizes.sort(reverse=True)
    
    result = 1
    for size in basin_sizes[:3]:
        result *= size
        
    return result
