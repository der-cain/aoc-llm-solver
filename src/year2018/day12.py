def parse(data):
    lines = data.strip().split('\n')
    initial_state_line = lines[0]
    initial_state = initial_state_line.split(': ')[1]

    rules = {}
    for line in lines[2:]:
        if '=>' in line:
            pattern, result = line.split(' => ')
            rules[pattern] = result

    # Convert state to a set of indices with plants
    state = set()
    for i, char in enumerate(initial_state):
        if char == '#':
            state.add(i)

    return state, rules

def step(state, rules):
    if not state:
        return set()

    min_idx = min(state)
    max_idx = max(state)

    new_state = set()

    # We need to check neighbors 2 to left and 2 to right.
    # So we iterate from min-2 to max+2.
    for i in range(min_idx - 2, max_idx + 3):
        # Build pattern
        pattern = ""
        for j in range(i - 2, i + 3):
            if j in state:
                pattern += "#"
            else:
                pattern += "."

        if rules.get(pattern, ".") == "#":
            new_state.add(i)

    return new_state

def calculate_sum(state):
    return sum(state)

def solve(state, rules, generations):
    # state and rules are already parsed
    seen_states = {}

    for gen in range(1, generations + 1):
        state = step(state, rules)

        if not state:
            return 0

        min_idx = min(state)
        # normalize by shifting min to 0
        normalized = tuple(sorted([x - min_idx for x in state]))

        if normalized in seen_states:
            prev_gen, prev_min = seen_states[normalized]
            period = gen - prev_gen
            shift = min_idx - prev_min

            if period == 1:
                remaining_gens = generations - gen
                final_sum = calculate_sum(state) + len(state) * shift * remaining_gens
                return final_sum

        seen_states[normalized] = (gen, min_idx)

    return calculate_sum(state)

def part1(data):
    state, rules = data
    return solve(state, rules, 20)

def part2(data):
    state, rules = data
    return solve(state, rules, 50000000000)
