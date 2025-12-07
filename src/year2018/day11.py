def get_power_level(x, y, serial):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = (power // 100) % 10
    power -= 5
    return power

def get_summed_area_table(serial, size=300):
    grid = [[0] * (size + 1) for _ in range(size + 1)]
    for y in range(1, size + 1):
        for x in range(1, size + 1):
            power = get_power_level(x, y, serial)
            grid[y][x] = power + grid[y-1][x] + grid[y][x-1] - grid[y-1][x-1]
    return grid

def get_total_power(sat, x, y, s):
    # Top-left (x, y), size s.
    # Indices in SAT:
    # (x+s-1, y+s-1) - (x-1, y+s-1) - (x+s-1, y-1) + (x-1, y-1)
    x0, y0 = x - 1, y - 1
    x1, y1 = x + s - 1, y + s - 1
    return sat[y1][x1] - sat[y1][x0] - sat[y0][x1] + sat[y0][x0]

def solve_max_power(serial, min_size=1, max_size=300):
    sat = get_summed_area_table(serial)
    max_power = -float('inf')
    best_id = None

    for s in range(min_size, max_size + 1):
        for y in range(1, 300 - s + 2):
            for x in range(1, 300 - s + 2):
                power = get_total_power(sat, x, y, s)
                if power > max_power:
                    max_power = power
                    best_id = (x, y, s)

    return best_id

def part1(data):
    serial = int(data)
    x, y, _ = solve_max_power(serial, 3, 3)
    return f"{x},{y}"

def part2(data):
    serial = int(data)
    x, y, s = solve_max_power(serial, 1, 300)
    return f"{x},{y},{s}"
