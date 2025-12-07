def parse(data):
    return [list(line) for line in data.strip().split('\n')]

def get_adj_stats(grid, x, y, rows, cols):
    trees = 0
    lumber = 0
    open_ = 0

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                cell = grid[ny][nx]
                if cell == '|':
                    trees += 1
                elif cell == '#':
                    lumber += 1
                elif cell == '.':
                    open_ += 1

    return open_, trees, lumber

def step(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [['' for _ in range(cols)] for _ in range(rows)]

    for y in range(rows):
        for x in range(cols):
            cell = grid[y][x]
            open_, trees, lumber = get_adj_stats(grid, x, y, rows, cols)

            if cell == '.':
                if trees >= 3:
                    new_grid[y][x] = '|'
                else:
                    new_grid[y][x] = '.'
            elif cell == '|':
                if lumber >= 3:
                    new_grid[y][x] = '#'
                else:
                    new_grid[y][x] = '|'
            elif cell == '#':
                if lumber >= 1 and trees >= 1:
                    new_grid[y][x] = '#'
                else:
                    new_grid[y][x] = '.'

    return new_grid

def calculate_value(grid):
    trees = sum(row.count('|') for row in grid)
    lumber = sum(row.count('#') for row in grid)
    return trees * lumber

def grid_to_string(grid):
    return '\n'.join(''.join(row) for row in grid)

def solve(grid, minutes):
    # grid is passed in (parsed list of lists)
    seen = {}
    history = []

    for m in range(minutes):
        s_grid = grid_to_string(grid)
        if s_grid in seen:
            pass # We handle cycle detection below
        else:
            seen[s_grid] = m
            history.append(grid)

        grid = step(grid)

        # Check cycle after step?
        s_next = grid_to_string(grid)
        if s_next in seen:
            first_seen_minute = seen[s_next]
            period = (m + 1) - first_seen_minute
            remaining = minutes - (m + 1)

            equiv_idx = first_seen_minute + (remaining % period)
            return calculate_value(history[equiv_idx])

    return calculate_value(grid)

def part1(data):
    # data is parsed grid
    return solve(data, 10)

def part2(data):
    # data is parsed grid
    return solve(data, 1000000000)
