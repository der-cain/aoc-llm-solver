def parse(data):
    parts = data.split("\n\n")
    algorithm = parts[0].replace("\n", "").strip()
    grid_lines = parts[1].strip().splitlines()
    
    pixels = set()
    for y, line in enumerate(grid_lines):
        for x, char in enumerate(line):
            if char == '#':
                pixels.add((x, y))
                
    return algorithm, pixels

def get_neighbors(x, y):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            yield x + dx, y + dy

def step(pixels, algorithm, default_pixel):
    # Calculate bounds
    if not pixels:
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
    else:
        min_x = min(p[0] for p in pixels)
        max_x = max(p[0] for p in pixels)
        min_y = min(p[1] for p in pixels)
        max_y = max(p[1] for p in pixels)
        
    new_pixels = set()
    
    # We need to expand 1 pixel outward from the bounding box
    # Because pixels outside the bounding box are 'default_pixel'.
    # A pixel at (min_x - 1, y) considers neighbors.
    # The 3x3 window around it might include some known pixels and some infinite default pixels.
    # If the algorithm maps 000000000 to 1 (#), then the infinite void turns on.
    # This toggles the 'default_pixel' state for the *next* iteration.
    
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            index = 0
            for nx, ny in get_neighbors(x, y):
                index <<= 1
                if (nx, ny) in pixels:
                    index |= 1
                elif default_pixel == '#':
                    # If infinite background is on, and pixel is not in our known set (but likely far away)
                    # wait. The known set 'pixels' contains ALL currently ON pixels?
                    # No, infinite pixels can calculate to infinite ON pixels.
                    # BUT, "flashing" infinite space is handled by tracking the 'default' value.
                    # We only track the 'exceptional' pixels in the set.
                    # If default is '.', we track '#'.
                    # If default is '#', we track '.'? Or we track '#' still?
                    # Let's assume we track '#' always.
                    # If default is '#', infinite space is '#'. 
                    # If we are effectively strictly bounded, we can just process the relevant area.
                    # If the infinite space flips, we need to know.
                    # Check algorithm[0] and algorithm[511].
                    # algorithm[0] tells us what ... (0) becomes.
                    # algorithm[511] tells us what ### (511) becomes.
                    
                    # If current default is '.', input 000...0 -> algo[0].
                    # If algo[0] is '#', infinite space turns ON.
                    # Next step default will be '#'.
                    # Then input 111...1 -> algo[511].
                    # If algo[511] is '.', infinite space turns OFF.
                    
                    # This implies valid puzzles toggle or stay off. They shouldn't stay ON forever and explode count.
                    # So we process bounds - 1 to +1.
                    # For any pixel outside these bounds, its neighbors are all 'default'.
                    # So it transitions to algo[0] (if default 0) or algo[511] (if default 1).
                    # This effectively updates the 'default' value.
                    
                    if not (min_x <= nx <= max_x and min_y <= ny <= max_y):
                         # It's truly outside our 'known' tracking bounds?
                         index |= 1
                    else:
                         # Inside bounds but not in set -> 0
                         pass
                else:
                    # default is '.', pixel not in set -> 0
                    pass
            
            if algorithm[index] == '#':
                new_pixels.add((x, y))
                
    # Determine new default
    if default_pixel == '.':
        # 0 -> algo[0]
        new_default = algorithm[0]
    else:
        # 511 -> algo[511]
        new_default = algorithm[511]
        
    return new_pixels, new_default

def part1(parsed_data):
    algorithm, pixels = parsed_data
    default_pixel = '.' # Initially dark
    
    for _ in range(2):
        pixels, default_pixel = step(pixels, algorithm, default_pixel)
        
    return len(pixels)

def part2(parsed_data):
    algorithm, pixels = parsed_data
    default_pixel = '.' # Initially dark
    
    for _ in range(50):
        pixels, default_pixel = step(pixels, algorithm, default_pixel)
        
    return len(pixels)
