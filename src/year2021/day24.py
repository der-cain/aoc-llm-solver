def parse(data):
    # Splits instructions into 14 chunks, one per 'inp w'
    lines = data.strip().splitlines()
    chunks = []
    current_chunk = []
    for line in lines:
        if line.startswith('inp') and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
        current_chunk.append(line)
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def extract_params(chunk):
    # Extract the 3 parameters that vary between chunks
    # div z A
    # add x B
    # add y C
    
    # Typically:
    # Line 4: div z A
    # Line 5: add x B
    # Line 15: add y C
    
    # Let's verify indices.
    # 0: inp w
    # ...
    # 4: div z A
    # 5: add x B
    # ...
    # 15: add y C
    
    a = int(chunk[4].split()[-1])
    b = int(chunk[5].split()[-1])
    c = int(chunk[15].split()[-1])
    return a, b, c

def solve_monad(chunks, maximize=True):
    # Stack-based derivation of constraints.
    # z acts as a stack of digits in base 26.
    # "push" operation: z = z * 26 + w + C
    # "pop" operation: z = z // 26
    # Condition to push or pop depends on x check: (z % 26) + B != w
    
    constraints = {} # index -> (pair_index, diff) meaning inputs[index] = inputs[pair_index] + diff
    stack = []
    
    for i, chunk in enumerate(chunks):
        div_z, add_x, add_y = extract_params(chunk)
        
        if div_z == 1:
            # Pushing to stack
            stack.append((i, add_y))
        elif div_z == 26:
            # Popping from stack
            prev_idx, prev_add_y = stack.pop()
            diff = prev_add_y + add_x
            constraints[i] = (prev_idx, diff)
            constraints[prev_idx] = (i, -diff)
            
    # Now reconstruct the model number
    model_num = [0] * 14
    
    # Process pairs
    # constraints contains both directions, careful not to double process
    processed = set()
    
    for i in range(14):
        if i in processed:
            continue
            
        j, diff = constraints[i]
        # i = j + diff
        # We want to determine inputs[i] and inputs[j]
        # range 1..9
        
        # If maximize:
        # Pick largest possible inputs[j] such that inputs[i] is valid
        # inputs[i] <= 9 => inputs[j] + diff <= 9 => inputs[j] <= 9 - diff
        # inputs[i] >= 1 => inputs[j] + diff >= 1 => inputs[j] >= 1 - diff
        
        # Combined: max(1, 1-diff) <= inputs[j] <= min(9, 9-diff)
        
        if maximize:
            val_j = min(9, 9 - diff)
        else:
            val_j = max(1, 1 - diff)
            
        val_i = val_j + diff
        
        model_num[i] = val_i
        model_num[j] = val_j
        
        processed.add(i)
        processed.add(j)
        
    return "".join(map(str, model_num))

def part1(parsed_data):
    return solve_monad(parsed_data, maximize=True)

def part2(parsed_data):
    # Problem will ask for smallest model number probably
    # Based on previous years/patterns.
    # The solver handles maximize=False.
    return solve_monad(parsed_data, maximize=False)
