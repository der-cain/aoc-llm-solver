from collections import deque
import copy

def parse(data):
    grid = [list(line) for line in data.split('\n') if line]
    units = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in ['G', 'E']:
                units.append({
                    'x': x,
                    'y': y,
                    'type': cell,
                    'hp': 200,
                    'id': len(units),
                    'active': True
                })
                grid[y][x] = '.' # Clear unit from grid to make movement easier

    return grid, units

def get_neighbors(x, y):
    # Reading order for ties is usually handled by scanning neighbors in reading order
    # Up, Left, Right, Down
    return [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]

def get_targets(unit, units):
    targets = []
    for other in units:
        if other['active'] and other['type'] != unit['type']:
            targets.append(other)
    return targets

def is_adjacent(u1, u2):
    return abs(u1['x'] - u2['x']) + abs(u1['y'] - u2['y']) == 1

def bfs_move(unit, targets, grid, units):
    # Identify in-range squares
    in_range = set()
    occupied = set()
    for u in units:
        if u['active']:
            occupied.add((u['x'], u['y']))

    for t in targets:
        for nx, ny in get_neighbors(t['x'], t['y']):
            if grid[ny][nx] == '.' and (nx, ny) not in occupied:
                in_range.add((nx, ny))

    if not in_range:
        return None

    # BFS to find reachable squares
    # We need: nearest (fewest steps), then reading order
    # BFS naturally finds nearest.
    # To handle reading order for *destination*:
    # Collect all reachable nodes at min_dist. Sort them by reading order. Pick first.

    start = (unit['x'], unit['y'])
    queue = deque([(start, 0)]) # (pos, dist)
    visited = {start: 0}

    # We want to find ALL reachable squares and their distances
    reachable_in_range = []
    min_dist_found = float('inf')

    while queue:
        (curr_x, curr_y), dist = queue.popleft()

        if dist > min_dist_found:
            break

        if (curr_x, curr_y) in in_range:
            reachable_in_range.append(((curr_x, curr_y), dist))
            min_dist_found = dist

        for nx, ny in get_neighbors(curr_x, curr_y):
            if grid[ny][nx] == '.' and (nx, ny) not in occupied and (nx, ny) not in visited:
                visited[(nx, ny)] = dist + 1
                queue.append(((nx, ny), dist + 1))

    if not reachable_in_range:
        return None

    # Sort by reading order (y, x)
    reachable_in_range.sort(key=lambda item: (item[0][1], item[0][0]))
    chosen_dest = reachable_in_range[0][0]

    # Now verify the step to take.
    # "If multiple steps would put the unit equally closer to its destination, the unit chooses the step which is first in reading order."
    # We do a reverse BFS from chosen_dest to start to find the first step?
    # Or BFS from start again, but checking which neighbor leads to chosen_dest with shortest path.

    # Let's BFS from start to find distances to chosen_dest via each neighbor
    # Actually, simpler: check each neighbor of start. If it can reach chosen_dest in (dist - 1), it's a candidate.
    # Pick candidate in reading order.

    # We need distance map from start to everywhere? We have `visited` but that's BFS order.
    # Re-run BFS from dest to start to get true distances is safer.

    # BFS from dest
    d_queue = deque([(chosen_dest, 0)])
    d_visited = {chosen_dest: 0}

    while d_queue:
        (cx, cy), d = d_queue.popleft()
        if (cx, cy) == start:
            break # Reached start

        for nx, ny in get_neighbors(cx, cy):
             if grid[ny][nx] == '.' and (nx, ny) not in occupied and (nx, ny) not in d_visited:
                 d_visited[(nx, ny)] = d + 1
                 d_queue.append(((nx, ny), d + 1))

    # Now check neighbors of start
    best_step = None
    min_step_dist = float('inf')

    for nx, ny in get_neighbors(start[0], start[1]):
        if (nx, ny) in d_visited:
            d = d_visited[(nx, ny)]
            if d < min_step_dist:
                min_step_dist = d
                best_step = (nx, ny)
            # Since neighbors are iterated in reading order, ties are already handled?
            # Yes, get_neighbors returns Up, Left, Right, Down.
            # Reading order: (y, x).
            # Up: (x, y-1). Left: (x-1, y). Right: (x+1, y). Down: (x, y+1).
            # (x, y-1) < (x-1, y)? y-1 < y. Yes.
            # (x-1, y) < (x+1, y)? x-1 < x+1. Yes.
            # (x+1, y) < (x, y+1)? y < y+1. Yes.
            # So the order Up, Left, Right, Down is exactly Reading Order.
            # So the first one we find with min_dist is the correct one.

    return best_step

def solve_combat(parsed_data, elf_attack=3, stop_on_elf_death=False):
    # Deep copy needed because state is mutated
    grid = copy.deepcopy(parsed_data[0])
    units = copy.deepcopy(parsed_data[1])

    rounds = 0

    while True:
        # Sort units by reading order
        units.sort(key=lambda u: (u['y'], u['x']))

        full_round = True

        for i, unit in enumerate(units):
            if not unit['active']:
                continue

            targets = get_targets(unit, units)
            if not targets:
                full_round = False
                break # Combat ends

            # Move if not adjacent
            adjacent_targets = [t for t in targets if is_adjacent(unit, t)]
            if not adjacent_targets:
                new_pos = bfs_move(unit, targets, grid, units)
                if new_pos:
                    unit['x'], unit['y'] = new_pos
                    # Check adjacency again after move
                    adjacent_targets = [t for t in targets if is_adjacent(unit, t)]

            # Attack
            if adjacent_targets:
                # Select target with fewest HP, then reading order
                adjacent_targets.sort(key=lambda t: (t['hp'], t['y'], t['x']))
                target = adjacent_targets[0]

                dmg = elf_attack if unit['type'] == 'E' else 3
                target['hp'] -= dmg

                if target['hp'] <= 0:
                    target['active'] = False
                    if stop_on_elf_death and target['type'] == 'E':
                        return None # Elf died

        # Filter dead units? No, we keep them but inactive, or remove them?
        # List modification during iteration is handled because we iterate by index or copy?
        # We iterate `units` list. If we remove items, indices shift.
        # But we sort at start of round. Dead units stay in list until next sort?
        # My loop uses `enumerate(units)`. If I remove from `units`, it breaks.
        # Better to keep them and check `active`.
        # Cleanup at end of round.
        units = [u for u in units if u['active']]

        if not full_round:
            break

        rounds += 1

    total_hp = sum(u['hp'] for u in units)
    return rounds * total_hp

def part1(data):
    return solve_combat(data)

def part2(data):
    # Binary search or linear search for min attack power?
    # Range isn't huge (starts 3). Linear is safer.
    attack = 4
    while True:
        outcome = solve_combat(data, elf_attack=attack, stop_on_elf_death=True)
        if outcome is not None:
            return outcome
        attack += 1
