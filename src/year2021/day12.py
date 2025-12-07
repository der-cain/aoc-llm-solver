from collections import defaultdict

def parse(data):
    adj = defaultdict(list)
    for line in data.splitlines():
        if not line.strip():
            continue
        u, v = line.strip().split('-')
        adj[u].append(v)
        adj[v].append(u)
    return adj

def count_paths(adj, u, visited):
    if u == 'end':
        return 1
    
    count = 0
    for v in adj[u]:
        if v.islower():
            if v not in visited:
                # Visit small cave
                new_visited = visited | {v}
                count += count_paths(adj, v, new_visited)
        else:
            # Visit big cave
            count += count_paths(adj, v, visited)
            
    return count

def part1(parsed_data):
    # 'start' is a small cave, so we mark it as visited initially
    return count_paths(parsed_data, 'start', {'start'})

def count_paths_part2(adj, u, visited, double_visit_used):
    if u == 'end':
        return 1
    
    count = 0
    for v in adj[u]:
        if v == 'start':
            continue
            
        if v.islower():
            if v not in visited:
                # First visit to this small cave
                new_visited = visited | {v}
                count += count_paths_part2(adj, v, new_visited, double_visit_used)
            else:
                # Visiting a small cave again
                if not double_visit_used:
                    # Allowed one double visit
                    count += count_paths_part2(adj, v, visited, True)
        else:
            # Big cave
            count += count_paths_part2(adj, v, visited, double_visit_used)
            
    return count

def part2(parsed_data):
    # 'start' is visited initially.
    # double_visit_used = False initially.
    return count_paths_part2(parsed_data, 'start', {'start'}, False)
