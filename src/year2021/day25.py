def parse(data):
    # Return grid as list of lists of chars
    return [list(line) for line in data.strip().splitlines()]

def step(grid):
    height = len(grid)
    width = len(grid[0])
    moved = False
    
    # East-facing herd
    new_grid = [row[:] for row in grid]
    for r in range(height):
        for c in range(width):
            if grid[r][c] == '>':
                next_c = (c + 1) % width
                if grid[r][next_c] == '.':
                    new_grid[r][next_c] = '>'
                    new_grid[r][c] = '.'
                    moved = True
    
    grid = new_grid
    
    # South-facing herd
    new_grid = [row[:] for row in grid]
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 'v':
                next_r = (r + 1) % height
                if grid[next_r][c] == '.':
                    new_grid[next_r][c] = 'v'
                    new_grid[r][c] = '.'
                    moved = True
                    
    return new_grid, moved

def part1(parsed_data):
    grid = parsed_data
    steps = 0
    while True:
        steps += 1
        grid, moved = step(grid)
        if not moved:
            return steps

def part2(parsed_data):
    return "Remotely Start The Sleigh"
