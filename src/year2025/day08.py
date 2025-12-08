from collections import defaultdict
import math

def parse(data):
    points = []
    for line in data.strip().split('\n'):
        parts = line.split(',')
        points.append(tuple(map(int, parts)))
    return points

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True
        return False

def part1(points):
    n = len(points)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            d2 = (points[i][0] - points[j][0])**2 + \
                 (points[i][1] - points[j][1])**2 + \
                 (points[i][2] - points[j][2])**2
            pairs.append((d2, i, j))

    # Sort by distance
    pairs.sort(key=lambda x: x[0])

    dsu = DSU(n)
    limit = 1000
    if n == 20: # Heuristic for example input
        limit = 10

    count = 0
    for _, i, j in pairs:
        dsu.union(i, j)
        count += 1
        if count == limit:
            break

    # Get component sizes
    sizes = []
    visited_roots = set()
    for i in range(n):
        root = dsu.find(i)
        if root not in visited_roots:
            sizes.append(dsu.size[root])
            visited_roots.add(root)

    sizes.sort(reverse=True)

    if len(sizes) < 3:
        # Fallback if fewer than 3 components (should not happen for large input/small K)
        # But if it does, we multiply available ones?
        # "multiply together the sizes of the three largest circuits"
        # If there is only 1 circuit, the answer is its size.
        ans = 1
        for s in sizes:
            ans *= s
        return ans

    return sizes[0] * sizes[1] * sizes[2]

def part2(points):
    n = len(points)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            d2 = (points[i][0] - points[j][0])**2 + \
                 (points[i][1] - points[j][1])**2 + \
                 (points[i][2] - points[j][2])**2
            pairs.append((d2, i, j))

    # Sort by distance
    pairs.sort(key=lambda x: x[0])

    dsu = DSU(n)
    components = n

    for _, i, j in pairs:
        if dsu.union(i, j):
            components -= 1
            if components == 1:
                return points[i][0] * points[j][0]
    return None
