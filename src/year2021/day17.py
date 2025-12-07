import re

def parse(data):
    # target area: x=20..30, y=-10..-5
    m = re.match(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", data.strip())
    if not m:
        raise ValueError("Invalid input format")
    x1, x2, y1, y2 = map(int, m.groups())
    return (x1, x2), (y1, y2)

def simulate(vx, vy, target_x_range, target_y_range):
    x, y = 0, 0
    max_y = 0
    x1, x2 = target_x_range
    y1, y2 = target_y_range
    
    # Simulate steps
    while True:
        x += vx
        y += vy
        max_y = max(max_y, y)
        
        # Check target
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True, max_y
            
        # Check overshoot/miss
        # If x is beyond x2 (assuming positive x target and positive vx, which usually holds for part 1)
        # If y is below y1 (assuming negative y target)
        if x > x2 and vx >= 0:
            return False, max_y
        if y < y1 and vy <= 0:
            return False, max_y
            
        # Drag
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        # Gravity
        vy -= 1
        
    return False, max_y

def part1(parsed_data):
    (x1, x2), (y1, y2) = parsed_data
    
    # Brute force search for velocities?
    # Or analytical?
    # Max initial vy produces max height.
    # If vy is large positive, it goes up, stops, comes down.
    # When it comes down to y=0, its velocity is -vy_initial - 1.
    # The next step will take it to y = -vy_initial - 1.
    # For maximum height, we want the largest vy_initial such that the probe doesn't overshoot the bottom of the target (y1).
    # Specifically, when passing y=0 downwards, the next step size must be at most abs(y1) (if landing exactly on y1)
    # Actually, the probe hits y=0 with velocity -v0-1.
    # The next position is 0 + (-v0 - 1) = -v0 - 1.
    # We need this to fall within [y1, y2]. Since y1 is negative bottom, we need it to land >= y1.
    # Wait, the step landing could be anywhere in [y1, y2].
    # But usually the maximum velocity is constrained by the bottom edge y1.
    # The fastest we can go down from y=0 and hit the target is to hit y1 in one step.
    # So next position -v0-1 >= y1.
    # Max v0 = abs(y1) - 1.
    # Let's verify this hypothesis with brute force on a reasonable range.
    
    best_max_y = 0
    
    # Search ranges:
    # vx: needs to reach x1 at least. sum(1..n) >= x1.
    # Also vx can't be too huge or it overshoots x2 in step 1.
    # vy: ranges from y1 (shoot down) to abs(y1) (shoot up).
    
    for vx in range(1, x2 + 2):
        for vy in range(y1, abs(y1) + 200): # A bit of buffer
            hit, max_y = simulate(vx, vy, (x1, x2), (y1, y2))
            if hit:
                best_max_y = max(best_max_y, max_y)
                
    return best_max_y

def part2(parsed_data):
    (x1, x2), (y1, y2) = parsed_data
    count = 0
    # Search ranges
    # vx: 1 to x2 (if > x2, overshoots in step 1)
    # vy: y1 to abs(y1) (if < y1, overshoots in step 1. if > abs(y1), overshoots on return trip)
    
    # Check if we need to expand search range for strict correctness?
    # Max vy bound is derived from: when falling passed y=0, vel is -(v0+1).
    # Step size is v0+1. If v0+1 > abs(y1), it might jump over the target.
    # So v0 approx abs(y1).
    
    for vx in range(1, x2 + 2):
        for vy in range(y1, abs(y1) + 200):
            hit, _ = simulate(vx, vy, (x1, x2), (y1, y2))
            if hit:
                count += 1
                
    return count
