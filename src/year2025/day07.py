def parse(data):
    grid = [list(line) for line in data.splitlines()]
    return grid

def solve_part1(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
            
    if not start_pos:
        return 0
        
    queue = [start_pos]
    visited = {start_pos}
    splitters_hit = 0
    activated_splitters = set()
    
    while queue:
        r, c = queue.pop(0)
        
        cell = grid[r][c]
        
        if cell == '^':
            if (r, c) not in activated_splitters:
                splitters_hit += 1
                activated_splitters.add((r, c))
            
            # Split: Left and Right
            # Note: The problem says beams "continue from" left and right.
            # Effectively, beam enters those cells.
            neighbors = [(r, c-1), (r, c+1)]
            for nr, nc in neighbors:
                if 0 <= nr < rows and 0 <= nc < cols:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
        else:
            # '.' or 'S' (treat S as empty space after start)
            # Beam moves downward
            nr, nc = r + 1, c
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    
    return splitters_hit

def part1(parsed_data):
    return solve_part1(parsed_data)

def part2(parsed_data):
    grid = parsed_data
    rows = len(grid)
    cols = len(grid[0])
    
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
            
    if not start_pos:
        return 0
        
    memo = {}
    
    def count_timelines(r, c):
        # Check bounds: any exit counts as 1 completed timeline
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return 1
            
        state = (r, c)
        if state in memo:
            return memo[state]
            
        cell = grid[r][c]
        
        res = 0
        if cell == '^':
            # Split: time splits into two timelines.
            # One goes left, one goes right.
            # They effectively "enter" the left and right cells.
            res = count_timelines(r, c - 1) + count_timelines(r, c + 1)
        else:
            # '.' or 'S'
            # Continues downward
            res = count_timelines(r + 1, c)
            
        memo[state] = res
        return res
        
    return count_timelines(start_pos[0], start_pos[1])
