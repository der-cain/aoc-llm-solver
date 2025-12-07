def parse(data):
    coords = []
    for line in data.splitlines():
        x, y = map(int, line.split(', '))
        coords.append((x, y))
    return coords

def part1(data):
    coords = data
    min_x = min(x for x, y in coords)
    max_x = max(x for x, y in coords)
    min_y = min(y for x, y in coords)
    max_y = max(y for x, y in coords)

    # Grid size needs to be large enough to contain all finite areas.
    # The bounding box of the points is a safe bet for determining finite vs infinite.
    # If an area touches the border of the bounding box, it's likely infinite.

    infinite_ids = set()
    counts = {}

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            min_dist = float('inf')
            closest_id = None

            for i, (cx, cy) in enumerate(coords):
                dist = abs(x - cx) + abs(y - cy)
                if dist < min_dist:
                    min_dist = dist
                    closest_id = i
                elif dist == min_dist:
                    closest_id = None

            if closest_id is not None:
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    infinite_ids.add(closest_id)
                counts[closest_id] = counts.get(closest_id, 0) + 1

    max_area = 0
    for i in range(len(coords)):
        if i not in infinite_ids:
            max_area = max(max_area, counts.get(i, 0))

    return max_area

def part2(data):
    coords = data
    min_x = min(x for x, y in coords)
    max_x = max(x for x, y in coords)
    min_y = min(y for x, y in coords)
    max_y = max(y for x, y in coords)

    # We might need to check slightly outside the bounding box,
    # but for total distance < 10000, and points spread out,
    # the region should be somewhat contained.
    # However, to be safe, we can expand the bounding box.
    # The max distance from the bounding box could be related to 10000 / len(coords).

    limit = 10000
    margin = limit // len(coords) + 1

    region_size = 0

    for x in range(min_x - margin, max_x + margin + 1):
        for y in range(min_y - margin, max_y + margin + 1):
            total_dist = sum(abs(x - cx) + abs(y - cy) for cx, cy in coords)
            if total_dist < limit:
                region_size += 1

    return region_size
