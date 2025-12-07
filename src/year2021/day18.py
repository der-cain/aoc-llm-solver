import math
import json
import copy

# Flat representation: list of [depth, value]
# Example: [[1,2],3] -> [[2,1], [2,2], [1,3]]

def parse_flat(data):
    flat = []
    def traverse(node, depth):
        if isinstance(node, int):
            flat.append([depth, node])
        else:
            traverse(node[0], depth + 1)
            traverse(node[1], depth + 1)
            
    traverse(json.loads(data), 0)
    return flat

def add_flat(l1, l2):
    # Deep copy needed? Integers are immutable, lists of [d,v] are mutable.
    # Create new list with incremented depths
    res = []
    for d, v in l1:
        res.append([d + 1, v])
    for d, v in l2:
        res.append([d + 1, v])
    return res

def explode_flat(flat):
    for i in range(len(flat)):
        depth, value = flat[i]
        if depth > 4:
            # Found left part of exploding pair
            # Right part must be i+1
            # Assert flat[i+1][0] == depth?
            
            left_val = value
            right_val = flat[i+1][1]
            
            # Add to left neighbor
            if i > 0:
                flat[i-1][1] += left_val
            
            # Add to right neighbor
            if i + 2 < len(flat):
                flat[i+2][1] += right_val
                
            # Replace current two with 0 at depth-1
            flat[i] = [depth - 1, 0]
            del flat[i+1]
            
            return True
    return False

def split_flat(flat):
    for i in range(len(flat)):
        depth, value = flat[i]
        if value >= 10:
            left_val = value // 2
            right_val = (value + 1) // 2
            
            flat[i] = [depth + 1, left_val]
            flat.insert(i + 1, [depth + 1, right_val])
            return True
            
    return False

def reduce_flat(flat):
    while True:
        if explode_flat(flat):
            continue
        if split_flat(flat):
            continue
        break
    return flat

def magnitude_flat(flat):
    # Iterative reduction of magnitude calculation?
    # Or recursive.
    # To do it recursively with flat structure, we can pass iterator?
    
    # Or destructive reduction: find deepest pair, calculate mag, replace.
    # Since mag calculation doesn't depend on depth value (only relative structure),
    # we can process depths max to min.
    
    # Actually, simpler:
    # Look for pair with same depth that are adjacent.
    # magnitude is 3*left + 2*right.
    # Replace with [depth-1, mag].
    # Repeat until one element.
    
    # Work on a copy
    work = [list(x) for x in flat]
    
    while len(work) > 1:
        # Find deepest depth
        max_d = max(x[0] for x in work)
        
        # Find first pair at max_d
        for i in range(len(work) - 1):
            if work[i][0] == max_d and work[i+1][0] == max_d:
                mag = 3 * work[i][1] + 2 * work[i+1][1]
                work[i] = [max_d - 1, mag]
                del work[i+1]
                break
                
    return work[0][1]

def parse(data):
    return [parse_flat(line) for line in data.splitlines() if line.strip()]

def part1(parsed_data):
    # parsed_data is list of flat lists
    if not parsed_data:
        return 0
        
    current = parsed_data[0]
    
    for next_num in parsed_data[1:]:
        current = add_flat(current, next_num)
        reduce_flat(current)
        
    return magnitude_flat(current)

def part2(parsed_data):
    # parsed_data is list of flat lists.
    # operations mutate them, so copy.
    
    max_mag = 0
    n = len(parsed_data)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
                
            n1 = [list(x) for x in parsed_data[i]] # Deep copy of list of lists
            n2 = [list(x) for x in parsed_data[j]]
            
            res = add_flat(n1, n2)
            reduce_flat(res)
            mag = magnitude_flat(res)
            
            if mag > max_mag:
                max_mag = mag
                
    return max_mag
