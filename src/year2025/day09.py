def parse(data):
    points = []
    for line in data.strip().split('\n'):
        if not line:
            continue
        x, y = map(int, line.split(','))
        points.append((x, y))
    return points

def part1(points):
    max_area = 0
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            if area > max_area:
                max_area = area
    return max_area

def part2(points):
    # Pre-calculate edges
    n = len(points)
    edges = []
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        edges.append((p1, p2))

    # Generate candidates
    candidates = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            candidates.append((area, x1, y1, x2, y2))

    # Sort by area descending
    candidates.sort(key=lambda x: x[0], reverse=True)

    # Check validity
    for area, rx1, ry1, rx2, ry2 in candidates:
        min_x, max_x = min(rx1, rx2), max(rx1, rx2)
        min_y, max_y = min(ry1, ry2), max(ry1, ry2)

        # 1. Check strict intersection with polygon edges
        intersect = False
        for p1, p2 in edges:
            ex1, ey1 = p1
            ex2, ey2 = p2

            # Normalize edge for intersection test
            e_min_x, e_max_x = min(ex1, ex2), max(ex1, ex2)
            e_min_y, e_max_y = min(ey1, ey2), max(ey1, ey2)

            is_vertical_edge = (ex1 == ex2)

            if is_vertical_edge:
                # Vertical edge at ex1. range [e_min_y, e_max_y]
                # Crosses R if min_x < ex1 < max_x AND y-intervals overlap strictly
                if min_x < ex1 < max_x:
                    # Check y overlap of (min_y, max_y) and (e_min_y, e_max_y)
                    overlap_start = max(min_y, e_min_y)
                    overlap_end = min(max_y, e_max_y)
                    if overlap_start < overlap_end:
                        intersect = True
                        break
            else:
                # Horizontal edge at ey1. range [e_min_x, e_max_x]
                if min_y < ey1 < max_y:
                    overlap_start = max(min_x, e_min_x)
                    overlap_end = min(max_x, e_max_x)
                    if overlap_start < overlap_end:
                        intersect = True
                        break

        if intersect:
            continue

        # 2. Check center point
        cx = (min_x + max_x) / 2
        cy = (min_y + max_y) / 2

        # Check if center is ON boundary
        on_boundary = False
        for p1, p2 in edges:
            ex1, ey1 = p1
            ex2, ey2 = p2
            # Check if (cx, cy) is on segment p1-p2
            if ex1 == ex2: # Vertical
                # Compare float cx to int ex1 with tolerance or direct if integer
                # Since ex1 is int, and cx can be .5, we need equality
                if abs(ex1 - cx) < 1e-9 and min(ey1, ey2) <= cy <= max(ey1, ey2):
                    on_boundary = True
                    break
            else: # Horizontal
                if abs(ey1 - cy) < 1e-9 and min(ex1, ex2) <= cx <= max(ex1, ex2):
                    on_boundary = True
                    break

        if on_boundary:
            return area

        # Ray casting
        # Ray from (cx, cy) to right
        # Perturb cy to avoid vertex issues: cy + epsilon
        test_y = cy + 0.001
        crossings = 0
        for p1, p2 in edges:
            ex1, ey1 = p1
            ex2, ey2 = p2

            # Check intersection with vertical edges
            if ex1 == ex2:
                # Vertical edge
                # Check if it spans test_y
                if min(ey1, ey2) < test_y < max(ey1, ey2):
                    # Check if it is to the right
                    if ex1 > cx:
                        crossings += 1

        if crossings % 2 == 1:
            return area

    return 0
