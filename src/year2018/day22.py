import heapq

def parse(data):
    lines = data.strip().split('\n')
    depth = int(lines[0].split(': ')[1])
    target = tuple(map(int, lines[1].split(': ')[1].split(',')))
    return depth, target

def get_erosion_level(x, y, depth, target, memo):
    if (x, y) in memo:
        return memo[(x, y)]

    geo_index = 0
    if (x, y) == (0, 0):
        geo_index = 0
    elif (x, y) == target:
        geo_index = 0
    elif y == 0:
        geo_index = x * 16807
    elif x == 0:
        geo_index = y * 48271
    else:
        # Recursion can be deep, so using loop or memo is key.
        # But we build up X and Y incrementally.
        # If we just compute on demand with memo, it should work fine if we process in order?
        # Actually, if we compute x=10, y=10, we need x=9,y=10 and x=10,y=9.
        # So we recurse. Recursion depth 1000 is fine.
        # But if target is large (e.g. 700, 700), recursion depth might be too much.
        # It's better to compute iteratively.
        # But for Part 1, we only need up to target.
        # For Part 2, we might go beyond.
        # Let's use memoized recursion with setrecursionlimit if needed, or iterative.
        # Iterative is safer.
        pass

    # Wait, recursive is problematic without pre-filling.
    # Let's assume we fill the grid as needed.
    # But since we don't know the bounds for Part 2, on-demand is better.
    # Let's use `memo` and if key missing, assume we fill dependencies?
    # No, dependencies must be computed.
    # We can't easily compute (x, y) without (x-1, y) and (x, y-1).
    # So we effectively need to fill a grid up to (x, y).

    # Let's stick to memoization but handle the recursion carefully or just ensure we iterate properly.
    # For now, let's implement the logic assuming we can fetch values.
    # If we run Dijkstra, we explore neighbors. (0,0) -> (1,0), (0,1).
    # So we always have neighbors computed if we go step by step?
    # Not necessarily. (1,1) needs (0,1) and (1,0). If we arrive at (1,1) from (0,1), we have (0,1). But we might not have (1,0) if we haven't visited it yet.
    # But for erosion level calculation, we need (1,0) even if we are at (0,1) and looking at (1,1).
    # So we must compute (1,0) on demand.

    # Given the math, we can compute column by column or row by row.
    # Or just use lru_cache.
    return 0 # Placeholder, logic moved to class or closure

class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.erosion = {}

    def get_erosion(self, x, y):
        if (x, y) in self.erosion:
            return self.erosion[(x, y)]

        geo_index = 0
        if (x, y) == (0, 0):
            geo_index = 0
        elif (x, y) == self.target:
            geo_index = 0
        elif y == 0:
            geo_index = x * 16807
        elif x == 0:
            geo_index = y * 48271
        else:
            geo_index = self.get_erosion(x-1, y) * self.get_erosion(x, y-1)

        erosion = (geo_index + self.depth) % 20183
        self.erosion[(x, y)] = erosion
        return erosion

    def get_type(self, x, y):
        # 0: rocky, 1: wet, 2: narrow
        return self.get_erosion(x, y) % 3

def part1(data):
    depth, target = data
    cave = Cave(depth, target)

    # Increase recursion limit just in case
    import sys
    sys.setrecursionlimit(5000)

    risk = 0
    for y in range(target[1] + 1):
        for x in range(target[0] + 1):
            risk += cave.get_type(x, y)

    return risk

def part2(data):
    depth, target = data
    cave = Cave(depth, target)

    import sys
    sys.setrecursionlimit(5000)

    # Dijkstra
    # State: (x, y, tool)
    # Tools: 0=Neither, 1=Torch, 2=Climbing Gear
    # Region Types: 0=Rocky, 1=Wet, 2=Narrow
    # Rules:
    # Rocky (0): Torch (1) or Gear (2). Cannot use Neither (0).
    # Wet (1): Gear (2) or Neither (0). Cannot use Torch (1).
    # Narrow (2): Torch (1) or Neither (0). Cannot use Gear (2).
    # Basically: Tool X is valid for Type Y if X != Y?
    # Rocky(0): 1!=0, 2!=0. Valid. 0==0 Invalid.
    # Wet(1): 2!=1, 0!=1. Valid. 1==1 Invalid.
    # Narrow(2): 1!=2, 0!=2. Valid. 2==2 Invalid.
    # So rule is: tool != region_type.

    # Start: (0, 0), Torch (1).
    # Target: target, Torch (1).

    queue = [(0, 0, 0, 1)] # (minutes, x, y, tool)
    visited = {} # (x, y, tool) -> minutes

    while queue:
        minutes, x, y, tool = heapq.heappop(queue)

        state = (x, y, tool)
        if state in visited and visited[state] <= minutes:
            continue
        visited[state] = minutes

        if (x, y) == target and tool == 1:
            return minutes

        # Try moving
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue

            region_type = cave.get_type(nx, ny)
            if tool != region_type: # Valid tool for new region
                heapq.heappush(queue, (minutes + 1, nx, ny, tool))

        # Try switching tool
        # Current region type
        curr_type = cave.get_type(x, y)
        for new_tool in [0, 1, 2]:
            if new_tool != tool and new_tool != curr_type:
                heapq.heappush(queue, (minutes + 7, x, y, new_tool))

    return -1
