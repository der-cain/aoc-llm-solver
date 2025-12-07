import collections
import itertools

def parse(data):
    scanners = []
    current_scanner = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("---"):
            if current_scanner:
                scanners.append(current_scanner)
            current_scanner = []
        else:
            current_scanner.append(tuple(map(int, line.split(','))))
    if current_scanner:
        scanners.append(current_scanner)
    return scanners

def get_orientations(point):
    x, y, z = point
    # 24 orientations
    # Logic: 
    # Face any of 6 directions (x, -x, y, -y, z, -z)
    # Rotate 0, 90, 180, 270 around that axis (4 rotations)
    # Total 24.
    
    # 1. Identity based
    yield (x, y, z)
    yield (y, -x, z)
    yield (-x, -y, z)
    yield (-y, x, z)
    
    # 2. Face -z (180 around x from z? No, rotate around y)
    # Rotate around y to bring z to -x?
    # Let's use permutations logic which is safer to implement
    # (x, y, z) -> permutations with signs such that det=1
    
    # Simple generator based on rolling:
    # roll: rotate around x
    # turn: rotate around z (or y)
    # https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
    
    # Manual list of 24 permutations
    yield (x, y, z)
    yield (y, z, x)
    yield (z, x, y)
    yield (-x, z, y)
    yield (z, y, -x)
    yield (y, -x, z)
    yield (x, z, -y)
    yield (z, -y, x)
    yield (-y, x, z)
    yield (x, -z, y)
    yield (-z, y, x)
    yield (y, x, -z)
    yield (-x, -y, z)
    yield (-y, -z, x)
    yield (-z, -x, -y)
    yield (x, -y, -z)
    yield (-y, -x, -z)
    yield (-x, -z, -y)
    yield (-z, -y, -x) # wait, det check
    # Maybe simpler to just implement roll/turn
    pass

# Hardcoded 24 rotations
# R(p) -> p'
ROTATIONS = [
    lambda p: (p[0], p[1], p[2]),
    lambda p: (p[0], p[2], -p[1]),
    lambda p: (p[0], -p[1], -p[2]),
    lambda p: (p[0], -p[2], p[1]),
    lambda p: (-p[0], -p[1], p[2]),
    lambda p: (-p[0], -p[2], -p[1]),
    lambda p: (-p[0], p[1], -p[2]),
    lambda p: (-p[0], p[2], p[1]),
    
    lambda p: (p[1], p[2], p[0]),
    lambda p: (p[1], p[0], -p[2]),
    lambda p: (p[1], -p[2], -p[0]),
    lambda p: (p[1], -p[0], p[2]),
    lambda p: (-p[1], -p[2], p[0]),
    lambda p: (-p[1], -p[0], -p[2]),
    lambda p: (-p[1], p[2], -p[0]),
    lambda p: (-p[1], p[0], p[2]),
    
    lambda p: (p[2], p[0], p[1]),
    lambda p: (p[2], p[1], -p[0]),
    lambda p: (p[2], -p[0], -p[1]),
    lambda p: (p[2], -p[1], p[0]),
    lambda p: (-p[2], -p[0], p[1]),
    lambda p: (-p[2], -p[1], -p[0]),
    lambda p: (-p[2], p[0], -p[1]),
    lambda p: (-p[2], p[1], p[0]),
]

def all_orientations(beacons):
    # Returns list of 24 lists of beacons
    return [[rot(b) for b in beacons] for rot in ROTATIONS]

def get_dist_sq(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2

def get_fingerprint(beacons):
    dists = set()
    n = len(beacons)
    for i in range(n):
        for j in range(i+1, n):
            dists.add(get_dist_sq(beacons[i], beacons[j]))
    return dists

def try_align(base_beacons, new_beacons_set_24):
    # Try to align new_beacons to base_beacons
    # Return (translated_beacons, scanner_pos) or None
    
    base_set = set(base_beacons)
    
    # Try each orientation
    for rotated_beacons in new_beacons_set_24:
        # Optimization: calculate difference counts
        # Map d -> count
        # d = base - rot
        diff_counts = collections.defaultdict(int)
        for b_rot in rotated_beacons:
            for b_base in base_beacons:
                diff = (b_base[0] - b_rot[0], b_base[1] - b_rot[1], b_base[2] - b_rot[2])
                diff_counts[diff] += 1
        
        # Check if any diff has >= 12 matches
        for diff, count in diff_counts.items():
            if count >= 12:
                # Found it!
                dx, dy, dz = diff
                translated = []
                for b in rotated_beacons:
                    translated.append((b[0]+dx, b[1]+dy, b[2]+dz))
                return translated, diff
                
    return None

def solve(scanners):
    n = len(scanners)
    fingerprints = [get_fingerprint(s) for s in scanners]
    
    # Cache all orientations for each scanner
    scanners_orientations = [all_orientations(s) for s in scanners]
    
    # State
    aligned_indices = {0}
    aligned_beacons = set(scanners[0])
    scanner_positions = {0: (0,0,0)} # Relative to 0
    final_beacons_per_scanner = {0: scanners[0]}
    
    queue = [0]
    
    while queue:
        base_idx = queue.pop(0)
        base_beacons = final_beacons_per_scanner[base_idx]
        base_fp = fingerprints[base_idx]
        
        for i in range(n):
            if i in aligned_indices:
                continue
                
            # Check overlap via fingerprint
            # Intersection of dist sets should be at least 12 choose 2 = 66
            # Actually, let's be generous, >= 66
            common_dists = len(base_fp.intersection(fingerprints[i]))
            if common_dists < 66:
                continue
                
            # Detailed check
            print(f"Checking {base_idx} vs {i} (common dists: {common_dists})")
            result = try_align(base_beacons, scanners_orientations[i])
            if result:
                translated_beacons, pos = result
                print(f"  Matched! Scanner {i} at {pos}")
                aligned_indices.add(i)
                scanner_positions[i] = pos
                final_beacons_per_scanner[i] = translated_beacons
                for b in translated_beacons:
                    aligned_beacons.add(b)
                queue.append(i)
                
    return aligned_beacons, scanner_positions

def part1(scanners):
    beacons, _ = solve(scanners)
    return len(beacons)

def part2(scanners):
    _, positions_map = solve(scanners)
    positions = list(positions_map.values())
    max_dist = 0
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            p1 = positions[i]
            p2 = positions[j]
            dist = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])
            max_dist = max(max_dist, dist)
    return max_dist
