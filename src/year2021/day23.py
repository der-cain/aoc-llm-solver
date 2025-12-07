import heapq

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_INDEX = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
ROOM_TARGETS = {2: 'A', 4: 'B', 6: 'C', 8: 'D'}

def parse(data):
    # Parse just the starting positions
    lines = data.strip().splitlines()
    # Lines 2 and 3 contain the amphipods (0-indexed lines)
    # Line 2: ###B#C#B#D### (indices 3,5,7,9 match rooms A,B,C,D)
    # Line 3:   #A#D#C#A#
    
    # We want a state like:
    # hallway: tuple of 11 chars ('.' or type)
    # rooms: tuple of 4 tuples (top, bottom)
    
    hallway = ('.',) * 11
    
    # Extract from lines
    row1 = lines[2].strip().replace('#', '')
    row2 = lines[3].strip().replace('#', '')
    
    # row1 is e.g. "BCBD"
    # row2 is e.g. "ADCA"
    
    rooms = (
        (row1[0], row2[0]), # A
        (row1[1], row2[1]), # B
        (row1[2], row2[2]), # C
        (row1[3], row2[3]), # D
    )
    
    return (hallway, rooms)

def get_possible_moves(state):
    hallway, rooms = state
    moves = []
    
    # 1. Move from hallway to room
    for h_idx, char in enumerate(hallway):
        if char == '.':
            continue
            
        target_room_idx = {'A':0, 'B':1, 'C':2, 'D':3}[char]
        target_room_h_idx = ROOM_INDEX[char]
        
        # Check path strictly between h_idx and target_room_h_idx
        # Exclude start h_idx
        step_dir = 1 if target_room_h_idx > h_idx else -1
        blocked = False
        for k in range(h_idx + step_dir, target_room_h_idx + step_dir, step_dir):
            if hallway[k] != '.':
                blocked = True
                break
        if blocked:
            continue
            
        # Check if room is valid (only contains target type or empty)
        room_content = rooms[target_room_idx]
        if any(c != '.' and c != char for c in room_content):
            continue
            
        # Determine slot in room (deepest empty)
        # room_content is (top, bottom) for Part 1
        # or (top, mid1, mid2, bottom) for Part 2
        dest_slot = -1
        for i in range(len(room_content) - 1, -1, -1):
            if room_content[i] == '.':
                dest_slot = i
                break
        
        if dest_slot == -1: # Room full
            continue
            
        # Execute move
        cost = (abs(h_idx - target_room_h_idx) + (dest_slot + 1)) * COSTS[char]
        
        new_hallway = list(hallway)
        new_hallway[h_idx] = '.'
        new_hallway = tuple(new_hallway)
        
        new_rooms = list(rooms)
        r_list = list(new_rooms[target_room_idx])
        r_list[dest_slot] = char
        new_rooms[target_room_idx] = tuple(r_list)
        new_rooms = tuple(new_rooms)
        
        yield (cost, (new_hallway, new_rooms))
        
    # 2. Move from room to hallway
    for r_idx, room in enumerate(rooms):
        # Check if room needs to empty
        target_type = ['A', 'B', 'C', 'D'][r_idx]
        if all(c == '.' or c == target_type for c in room):
            continue # Already sorted or empty, don't move out
            
        # Find top-most amphipod
        src_slot = -1
        char = '.'
        for i, c in enumerate(room):
            if c != '.':
                src_slot = i
                char = c
                break
        
        if src_slot == -1: # Empty room
            continue
            
        room_h_idx = [2, 4, 6, 8][r_idx]
        
        # Try all reachable hallway spots
        for h_idx in [0, 1, 3, 5, 7, 9, 10]:
            # Check path
            step_dir = 1 if h_idx > room_h_idx else -1
            blocked = False
            for k in range(room_h_idx + step_dir, h_idx + step_dir, step_dir):
                if hallway[k] != '.':
                    blocked = True
                    break
            if blocked:
                continue
                
            cost = (abs(h_idx - room_h_idx) + (src_slot + 1)) * COSTS[char]
            
            new_hallway = list(hallway)
            new_hallway[h_idx] = char
            new_hallway = tuple(new_hallway)
            
            new_rooms = list(rooms)
            r_list = list(new_rooms[r_idx])
            r_list[src_slot] = '.'
            new_rooms[r_idx] = tuple(r_list)
            new_rooms = tuple(new_rooms)
            
            yield (cost, (new_hallway, new_rooms))

def is_done(state):
    _, rooms = state
    targets = ['A', 'B', 'C', 'D']
    for i, room in enumerate(rooms):
        if any(c != targets[i] for c in room):
            return False
    return True

def solve_dijkstra(start_state):
    pq = [(0, start_state)]
    visited = {} # state -> cost
    visited[start_state] = 0
    
    min_cost = float('inf')
    
    while pq:
        cost, state = heapq.heappop(pq)
        
        if cost > visited.get(state, float('inf')):
            continue
            
        if is_done(state):
            return cost
            
        for d_cost, next_state in get_possible_moves(state):
            new_cost = cost + d_cost
            if new_cost < visited.get(next_state, float('inf')):
                visited[next_state] = new_cost
                heapq.heappush(pq, (new_cost, next_state))
                
    return -1

def part1(parsed_data):
    return solve_dijkstra(parsed_data)

def part2(parsed_data):
    # Part 2 injects lines
    # #D#C#B#A#
    # #D#B#A#C#
    # into the rooms
    hallway, rooms = parsed_data
    
    # Insert new lines
    # Room A: (top, bottom) -> (top, 'D', 'D', bottom)
    # Room B: (top, bottom) -> (top, 'C', 'B', bottom)
    # etc
    
    extra_rows = [
        ('D', 'D'),
        ('C', 'B'),
        ('B', 'A'),
        ('A', 'C'),
    ]
    
    new_rooms = []
    for i, r in enumerate(rooms):
        top, bottom = r
        new_rooms.append((top, extra_rows[i][0], extra_rows[i][1], bottom))
        
    start_state = (hallway, tuple(new_rooms))
    return solve_dijkstra(start_state)
