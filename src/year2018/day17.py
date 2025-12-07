import sys
sys.setrecursionlimit(20000)

def parse(data):
    clay = set()
    for line in data.strip().split('\n'):
        parts = line.split(', ')
        first = parts[0].split('=')
        second = parts[1].split('=')

        c1_val = int(first[1])
        c2_range = list(map(int, second[1].split('..')))

        if first[0] == 'x':
            x = c1_val
            for y in range(c2_range[0], c2_range[1] + 1):
                clay.add((x, y))
        else:
            y = c1_val
            for x in range(c2_range[0], c2_range[1] + 1):
                clay.add((x, y))

    return clay

def solve(clay):
    if not clay:
        return 0, 0

    min_y = min(y for x, y in clay)
    max_y = max(y for x, y in clay)

    water = set()
    settled = set()

    def fill(x, y):
        if y > max_y:
            return

        if (x, y) in clay:
            return

        if (x, y) not in water:
            water.add((x, y))

        if (x, y) in settled:
            return

        # Down
        down = (x, y + 1)
        if down not in clay and down not in settled:
            if down not in water:
                fill(x, y + 1)

            # Recheck because fill might have settled it
            if down not in settled:
                return

        # Spread left
        left = x
        left_spilled = False
        while True:
            water.add((left, y))
            below = (left, y + 1)

            if below not in clay and below not in settled:
                # Potential spill
                if below not in water:
                    fill(left, y + 1)

                # Check if it settled
                if below in settled:
                    # Plugged! Continue spreading
                    pass
                else:
                    # Still open, so it's a real spill
                    left_spilled = True
                    break

            if (left - 1, y) in clay:
                break
            left -= 1

        # Spread right
        right = x
        right_spilled = False
        while True:
            water.add((right, y))
            below = (right, y + 1)

            if below not in clay and below not in settled:
                if below not in water:
                    fill(right, y + 1)

                if below in settled:
                    pass
                else:
                    right_spilled = True
                    break

            if (right + 1, y) in clay:
                break
            right += 1

        if not left_spilled and not right_spilled:
            # Settle row
            for i in range(left, right + 1):
                settled.add((i, y))

    fill(500, 0)

    wet_count = sum(1 for (x, y) in water if min_y <= y <= max_y)
    settled_count = sum(1 for (x, y) in settled if min_y <= y <= max_y)

    return wet_count, settled_count

def part1(data):
    # data is already parsed by main.py -> it's 'clay' set
    wet, _ = solve(data)
    return wet

def part2(data):
    _, settled = solve(data)
    return settled
