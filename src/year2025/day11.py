from functools import lru_cache
import collections

def parse(input_data: str):
    return parse_input(input_data)

def part1(graph):
    return count_paths(graph)

def part2(graph):
    # Paths visiting both dac and fft
    # Order 1: svr -> dac -> fft -> out
    p1 = count_paths(graph, 'svr', 'dac') * count_paths(graph, 'dac', 'fft') * count_paths(graph, 'fft', 'out')
    
    # Order 2: svr -> fft -> dac -> out
    p2 = count_paths(graph, 'svr', 'fft') * count_paths(graph, 'fft', 'dac') * count_paths(graph, 'dac', 'out')
    
    return p1 + p2


def parse_input(input_data: str):
    graph = collections.defaultdict(list)
    for line in input_data.strip().split('\n'):
        if not line:
            continue
        parts = line.split(':')
        source = parts[0].strip()
        destinations = parts[1].strip().split()
        graph[source] = destinations
    return graph

def count_paths(graph, start='you', end='out'):
    @lru_cache(None)
    def dfs(current_node):
        if current_node == end:
            return 1
        
        count = 0
        if current_node in graph:
            for neighbor in graph[current_node]:
                count += dfs(neighbor)
        return count

    return dfs(start)

