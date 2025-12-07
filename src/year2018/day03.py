import re

def parse(data):
    claims = []
    # #1 @ 1,3: 4x4
    pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    for line in data.splitlines():
        match = pattern.match(line)
        if match:
            claims.append(tuple(map(int, match.groups())))
    return claims

def part1(data):
    fabric = {}
    for _, x, y, w, h in data:
        for i in range(x, x + w):
            for j in range(y, y + h):
                fabric[(i, j)] = fabric.get((i, j), 0) + 1

    return sum(1 for v in fabric.values() if v >= 2)

def part2(data):
    fabric = {}
    for id, x, y, w, h in data:
        for i in range(x, x + w):
            for j in range(y, y + h):
                fabric[(i, j)] = fabric.get((i, j), 0) + 1

    for id, x, y, w, h in data:
        overlap = False
        for i in range(x, x + w):
            for j in range(y, y + h):
                if fabric[(i, j)] > 1:
                    overlap = True
                    break
            if overlap:
                break
        if not overlap:
            return id
