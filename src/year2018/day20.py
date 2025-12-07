from collections import deque, defaultdict

def parse_regex(regex):
    # We essentially walk the regex and build the map (distance to each room)
    # Since we want shortest path, and the regex describes paths, we can just follow them.
    # The map is a graph. Rooms are nodes.
    # We can store min_dist to each room.

    # Or better: Just traverse the regex and update distances.
    # Stack stores (x, y) positions for branching.

    distances = defaultdict(lambda: float('inf'))
    start = (0, 0)
    distances[start] = 0

    x, y = 0, 0
    stack = [] # Stores list of (x, y) to return to

    # We need to iterate carefully.
    # Actually, the regex describes paths.
    # `(` pushes current pos to stack.
    # `|` resets pos to stack.top (but doesn't pop).
    # `)` pops from stack.
    # Directions update x, y and update distance.

    # Wait, `(A|B)` means from current point P, we can go A -> P1 or B -> P2.
    # Both P1 and P2 are valid endpoints of this group.
    # `(A|B)C` means we go A -> P1 -> C ... AND B -> P2 -> C ...
    # Wait. Is it?
    # Example: `^N(E|W)N$` -> N -> (E or W) -> N.
    # N -> P1.
    # P1 -> E -> P2. Then P2 -> N.
    # P1 -> W -> P3. Then P3 -> N.
    # So `)` implies we continue from ALL endpoints of the group?
    # Usually in AoC regex inputs for map generation (like this specific problem),
    # the branches loop back or end dead?
    # Let's check `^ENWWW(NEEE|SSE(EE|N))$`.
    # ENWWW -> P1.
    # Branch 1: NEEE -> End.
    # Branch 2: SSE...
    # The regex ends after `)`.
    # What about `(NEWS|WNSE|)SSSEEN`?
    # (NEWS|) -> Option 1: NEWS -> P2. Option 2: Empty -> P1.
    # Then SSSEEN continues from P2 AND P1?
    # Yes.

    # So we need to track a SET of current positions?
    # No, usually these problems can be solved by simple recursion or stack.
    # But `|` resets to the start of the group.
    # `)` needs to collect all endpoints?
    # If I just maintain `current_positions` set?

    current_positions = {start}
    stack = [] # Stores sets of positions

    # For simple implementation, let's treat the regex as a walk.
    # When we hit `(`, we save current_positions.
    # When we hit `|`, we restore start_positions (of the group) but we also need to keep the endpoints of the previous branch.
    # When we hit `)`, the new current_positions is the union of endpoints of all branches.

    # Stack stores: (start_positions, collected_endpoints)

    idx = 0
    # Skip ^ and $
    path = regex[1:-1]

    for char in path:
        if char == '(':
            stack.append((current_positions, set()))
            # current_positions remains as is for the first branch
        elif char == '|':
            start_positions, endpoints = stack[-1]
            endpoints.update(current_positions)
            current_positions = start_positions # Reset for next branch
            # Note: `start_positions` should be a copy if we modified it?
            # `current_positions` is a set. `start_positions` is reference to set from push time.
            # If we modify `current_positions` in place, `start_positions` on stack will change?
            # Yes. So we must create new sets.
            # Let's verify loop logic below.
        elif char == ')':
            start_positions, endpoints = stack.pop()
            endpoints.update(current_positions)
            current_positions = endpoints
        else:
            # Move
            dx, dy = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}[char]
            next_positions = set()
            for x, y in current_positions:
                nx, ny = x + dx, y + dy
                dist = distances[(x, y)] + 1
                if dist < distances[(nx, ny)]:
                    distances[(nx, ny)] = dist
                # Even if we found a longer path, we record the node.
                # Actually, BFS/Dijkstra would effectively do this.
                # Here we are exploring ALL paths.
                # Since graph is a tree (usually) or at least we want shortest path dist:
                # `distances` map stores min_dist found SO FAR.
                # Since we process the string linearly, does it guarantee finding shortest?
                # No. `N(E|W)N` vs `NEN`.
                # If we have loops?
                # The problem says "The regex matches routes... mapping out all of these routes will let you build a proper map".
                # "routes will take you through every door in the facility at least once".
                # So the regex effectively traverses the Minimum Spanning Tree or something?
                # If there are cycles, the regex describes them.
                # `distances` update `min` is correct.
                # We just need to ensure `distances` tracks the shortest path distance.
                # Since steps are weight 1, `min` update is fine.
                next_positions.add((nx, ny))
            current_positions = next_positions

    return distances

def solve(data):
    distances = parse_regex(data.strip())
    return max(distances.values())

def part1(data):
    return solve(data)

def part2(data):
    distances = parse_regex(data.strip())
    return sum(1 for d in distances.values() if d >= 1000)
