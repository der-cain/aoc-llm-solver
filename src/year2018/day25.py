def parse(data):
    points = []
    for line in data.strip().split('\n'):
        points.append(tuple(map(int, line.split(','))))
    return points

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.num_sets = size

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            self.num_sets -= 1
            return True
        return False

def part1(data):
    points = data
    n = len(points)
    uf = UnionFind(n)

    # Compare all pairs. Optimized?
    # N is usually small (e.g. 1000). O(N^2) is 1M, totally fine.

    for i in range(n):
        for j in range(i + 1, n):
            if dist(points[i], points[j]) <= 3:
                uf.union(i, j)

    return uf.num_sets

def part2(data):
    # Usually requires 49 stars.
    return "Click The Button"
