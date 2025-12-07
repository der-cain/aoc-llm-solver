import copy

def parse(data):
    grid = [list(line) for line in data.split('\n') if line]
    carts = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in ['^', 'v', '<', '>']:
                # Cart found
                # Direction: 0=Up, 1=Right, 2=Down, 3=Left
                direction = {'^': 0, '>': 1, 'v': 2, '<': 3}[cell]
                carts.append({
                    'x': x,
                    'y': y,
                    'dir': direction,
                    'turn': 0, # 0=Left, 1=Straight, 2=Right
                    'id': len(carts),
                    'crashed': False
                })
                # Replace track under cart
                if cell in ['^', 'v']:
                    grid[y][x] = '|'
                elif cell in ['<', '>']:
                    grid[y][x] = '-'

    return grid, carts

def turn_cart(cart):
    # turn: 0=Left, 1=Straight, 2=Right
    if cart['turn'] == 0: # Left
        cart['dir'] = (cart['dir'] - 1) % 4
    elif cart['turn'] == 2: # Right
        cart['dir'] = (cart['dir'] + 1) % 4
    # 1=Straight: do nothing
    cart['turn'] = (cart['turn'] + 1) % 3

def move_carts(grid, carts, remove_crashed=False):
    carts.sort(key=lambda c: (c['y'], c['x']))
    crashes = []

    for cart in carts:
        if cart['crashed']:
            continue

        # Move
        dx, dy = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}[cart['dir']]
        cart['x'] += dx
        cart['y'] += dy

        # Check collision
        for other in carts:
            if other['id'] != cart['id'] and not other['crashed']:
                if other['x'] == cart['x'] and other['y'] == cart['y']:
                    crashes.append((cart['x'], cart['y']))
                    cart['crashed'] = True
                    other['crashed'] = True
                    break

        if cart['crashed']:
            continue

        # Handle track
        cell = grid[cart['y']][cart['x']]
        if cell == '+':
            turn_cart(cart)
        elif cell == '/':
            # Up (0) -> Right (1)
            # Right (1) -> Up (0)
            # Down (2) -> Left (3)
            # Left (3) -> Down (2)
            if cart['dir'] == 0: cart['dir'] = 1
            elif cart['dir'] == 1: cart['dir'] = 0
            elif cart['dir'] == 2: cart['dir'] = 3
            elif cart['dir'] == 3: cart['dir'] = 2
        elif cell == '\\':
            # Up (0) -> Left (3)
            # Left (3) -> Up (0)
            # Down (2) -> Right (1)
            # Right (1) -> Down (2)
            if cart['dir'] == 0: cart['dir'] = 3
            elif cart['dir'] == 1: cart['dir'] = 2
            elif cart['dir'] == 2: cart['dir'] = 1
            elif cart['dir'] == 3: cart['dir'] = 0

    if remove_crashed:
        carts[:] = [c for c in carts if not c['crashed']]

    return crashes

def part1(data):
    grid, carts = copy.deepcopy(data)
    while True:
        crashes = move_carts(grid, carts)
        if crashes:
            return f"{crashes[0][0]},{crashes[0][1]}"

def part2(data):
    grid, carts = copy.deepcopy(data)
    while len(carts) > 1:
        move_carts(grid, carts, remove_crashed=True)

    if carts:
        return f"{carts[0]['x']},{carts[0]['y']}"
    return "No carts left"
