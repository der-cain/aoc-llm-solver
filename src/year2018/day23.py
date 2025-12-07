import re

def parse(data):
    bots = []
    pattern = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")
    for line in data.strip().split('\n'):
        match = pattern.match(line)
        if match:
            bots.append(tuple(map(int, match.groups())))
    return bots

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

def part1(data):
    bots = data
    strongest = max(bots, key=lambda b: b[3])
    count = 0
    for bot in bots:
        if dist(strongest[:3], bot[:3]) <= strongest[3]:
            count += 1
    return count

def part2(data):
    # This is a classic "clique" or "intersection" problem in 3D.
    # We want to find a coordinate (x, y, z) that is in range of the MOST bots.
    # Tie-breaking: shortest distance to (0,0,0).

    # Octree / Divide and Conquer approach.
    # 1. Define a bounding box covering all bots.
    # 2. Split into 8 sub-cubes.
    # 3. For each sub-cube, count how many bots COULD cover a point in it.
    #    A bot covers a cube if the distance from bot to the cube is <= radius.
    #    Distance from bot to cube: max(0, bot.x - cube.max_x, cube.min_x - bot.x) + ...
    # 4. Priority Queue to explore cubes with most potential bots.
    # 5. When cube size is 1, we found a candidate.

    import heapq

    bots = data

    min_x = min(b[0] for b in bots)
    max_x = max(b[0] for b in bots)
    min_y = min(b[1] for b in bots)
    max_y = max(b[1] for b in bots)
    min_z = min(b[2] for b in bots)
    max_z = max(b[2] for b in bots)

    # Ensure power of 2 size for clean splitting
    size = max(max_x - min_x, max_y - min_y, max_z - min_z)
    power_of_2 = 1
    while power_of_2 <= size:
        power_of_2 *= 2

    # Queue: (-num_bots, distance_to_origin, size, x, y, z)
    # We use negative num_bots for max-heap behavior with heapq (which is min-heap)
    # distance_to_origin is tie-breaker (min preferred)

    queue = []

    def count_intersects(bx, by, bz, bsize):
        # Determine how many bots intersect with the cube defined by (bx, by, bz) and size
        count = 0
        for x, y, z, r in bots:
            # Manhattan distance from (x,y,z) to box
            d = 0
            if x < bx: d += bx - x
            elif x > bx + bsize - 1: d += x - (bx + bsize - 1)

            if y < by: d += by - y
            elif y > by + bsize - 1: d += y - (by + bsize - 1)

            if z < bz: d += bz - z
            elif z > bz + bsize - 1: d += z - (bz + bsize - 1)

            if d <= r:
                count += 1
        return count

    # Initial cube
    initial_count = count_intersects(min_x, min_y, min_z, power_of_2)
    # distance to origin
    # Closest point in box to origin
    # If origin inside box, 0. Else manhattan.
    # Actually, the problem asks for shortest distance from coordinate to 0,0,0.
    # So we want the coordinate itself.
    # The queue item represents a BOX. We use min_dist from box to origin as heuristic?
    # Yes.

    heapq.heappush(queue, (-initial_count, abs(min_x) + abs(min_y) + abs(min_z), power_of_2, min_x, min_y, min_z))
    # Note: Using box corner for dist is approximation, but with Priority Queue ordering by count first, it should work.
    # Actually, strictly we should use "min possible distance to origin from any point in box".
    # Since we split, eventually we get to size 1.

    while queue:
        neg_count, dist_orig, size, x, y, z = heapq.heappop(queue)

        if size == 1:
            return dist_orig # This is the coordinate's distance to origin

        new_size = size // 2

        # 8 sub-cubes
        for dx in [0, new_size]:
            for dy in [0, new_size]:
                for dz in [0, new_size]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    n_count = count_intersects(nx, ny, nz, new_size)
                    if n_count > 0:
                        # Min dist to origin from this box
                        # Coordinate closest to 0 in range [nx, nx+new_size-1]
                        cx = 0
                        if 0 < nx: cx = nx
                        elif 0 > nx + new_size - 1: cx = nx + new_size - 1

                        cy = 0
                        if 0 < ny: cy = ny
                        elif 0 > ny + new_size - 1: cy = ny + new_size - 1

                        cz = 0
                        if 0 < nz: cz = nz
                        elif 0 > nz + new_size - 1: cz = nz + new_size - 1

                        ndist = abs(cx) + abs(cy) + abs(cz)

                        heapq.heappush(queue, (-n_count, ndist, new_size, nx, ny, nz))

    return -1
