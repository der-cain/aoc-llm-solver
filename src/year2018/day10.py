import re

def parse(data):
    points = []
    pattern = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>")
    for line in data.strip().split('\n'):
        match = pattern.match(line)
        if match:
            points.append({
                'pos': [int(match.group(1)), int(match.group(2))],
                'vel': (int(match.group(3)), int(match.group(4)))
            })
    return points

def get_bounding_box(points):
    min_x = min(p['pos'][0] for p in points)
    max_x = max(p['pos'][0] for p in points)
    min_y = min(p['pos'][1] for p in points)
    max_y = max(p['pos'][1] for p in points)
    return min_x, max_x, min_y, max_y

def get_area(points):
    min_x, max_x, min_y, max_y = get_bounding_box(points)
    return (max_x - min_x) * (max_y - min_y)

def print_points(points):
    min_x, max_x, min_y, max_y = get_bounding_box(points)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    grid = [['.' for _ in range(width)] for _ in range(height)]

    for p in points:
        x = p['pos'][0] - min_x
        y = p['pos'][1] - min_y
        grid[y][x] = '#'

    return '\n'.join(''.join(row) for row in grid)

def solve(points):
    seconds = 0
    prev_area = float('inf')

    while True:
        # Move points
        for p in points:
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]

        seconds += 1
        area = get_area(points)

        if area > prev_area:
            # We passed the minimum. Revert one step.
            for p in points:
                p['pos'][0] -= p['vel'][0]
                p['pos'][1] -= p['vel'][1]
            return seconds - 1, print_points(points)

        prev_area = area

def part1(data):
    # This returns the visual message.
    import copy
    points_copy = copy.deepcopy(data)
    _, message = solve(points_copy)
    return "\n" + message

def part2(data):
    import copy
    points_copy = copy.deepcopy(data)
    seconds, _ = solve(points_copy)
    return seconds
