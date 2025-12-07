import re

def parse(data):
    steps = []
    # on x=10..12,y=10..12,z=10..12
    pattern = r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
    for line in data.splitlines():
        if not line.strip():
            continue
        match = re.search(pattern, line)
        if match:
            action = match.group(1)
            coords = list(map(int, match.groups()[1:]))
            # Store as x1, x2, y1, y2, z1, z2
            # Inclusive ranges
            steps.append((action, tuple(coords)))
    return steps

def get_intersection(c1, c2):
    # c1, c2 are tuples (x1, x2, y1, y2, z1, z2)
    # Return intersection tuple or None
    x1 = max(c1[0], c2[0])
    x2 = min(c1[1], c2[1])
    y1 = max(c1[2], c2[2])
    y2 = min(c1[3], c2[3])
    z1 = max(c1[4], c2[4])
    z2 = min(c1[5], c2[5])
    
    if x1 <= x2 and y1 <= y2 and z1 <= z2:
        return (x1, x2, y1, y2, z1, z2)
    return None

def solve(steps, bounds=None):
    # bounds: (min_val, max_val) applied to all dimensions
    
    cuboids = [] # List of (cuboid_tuple, sign)
    
    for action, coords in steps:
        # coords: x1, x2, y1, y2, z1, z2 inclusive
        
        # Apply bounds if needed (for Part 1)
        if bounds:
            b_min, b_max = bounds
            x1, x2, y1, y2, z1, z2 = coords
            
            # Check overlap with bounds
            if x2 < b_min or x1 > b_max or y2 < b_min or y1 > b_max or z2 < b_min or z1 > b_max:
                continue
                
            # Clamp
            x1 = max(x1, b_min)
            x2 = min(x2, b_max)
            y1 = max(y1, b_min)
            y2 = min(y2, b_max)
            z1 = max(z1, b_min)
            z2 = min(z2, b_max)
            coords = (x1, x2, y1, y2, z1, z2)
            
        new_cuboids = []
        
        # Add intersections to cancel overlaps
        for existing_c, sign in cuboids:
            intersect = get_intersection(existing_c, coords)
            if intersect:
                new_cuboids.append((intersect, -sign))
                
        # If adding "on", add the positive volume
        if action == "on":
            new_cuboids.append((coords, 1))
            
        cuboids.extend(new_cuboids)
        
    total_volume = 0
    for (x1, x2, y1, y2, z1, z2), sign in cuboids:
        vol = (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
        total_volume += sign * vol
        
    return total_volume

def part1(parsed_data):
    return solve(parsed_data, bounds=(-50, 50))

def part2(parsed_data):
    return solve(parsed_data, bounds=None)
