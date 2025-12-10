
import re
import math
from functools import reduce

def parse(data):
    """
    Parses the input data into a list of machines.
    Each machine is a tuple (target_vector, button_matrix, joltage_vector).
    target_vector: list of 0s and 1s representing required light states.
    button_matrix: list of lists, where each inner list represents a button's effect.
    joltage_vector: list of integers representing joltage requirements.
    """
    machines = []
    lines = data.strip().split('\n')
    
    for line in lines:
        if not line.strip():
            continue
            
        # Parse indicator light diagram [...]
        # Example: [.##.]
        diagram_match = re.search(r'\[([.#]+)\]', line)
        if not diagram_match:
            continue
        
        diagram_str = diagram_match.group(1)
        target = [1 if c == '#' else 0 for c in diagram_str]
        num_items = len(target)
        
        # Parse buttons (...)
        # Example: (3) (1,3) ...
        # Can have multiple parents groups
        # We can just find all matches for \(\d+(?:,\d+)*\) but careful about joltage
        # Joltage is {....}
        
        # Extract joltage part first
        joltage_match = re.search(r'\{([\d,]+)\}', line)
        if not joltage_match:
            continue # Should be there
        
        joltage_str = joltage_match.group(1)
        joltage = [int(x) for x in joltage_str.split(',')]
        
        # Remove joltage from line to avoid confusion
        line_no_joltage = line.replace(joltage_match.group(0), "")
        
        button_matches = re.findall(r'\(([\d,]+)\)', line_no_joltage)
        buttons = []
        for btn_str in button_matches:
            indices = [int(x) for x in btn_str.split(',')]
            button_vec = [0] * num_items
            for idx in indices:
                if 0 <= idx < num_items:
                    button_vec[idx] = 1
            buttons.append(button_vec)
            
        machines.append((target, buttons, joltage))
        
    return machines

def rref_gf2(matrix, augmented_col=None):
    """
    Computes RREF of a matrix over GF(2).
    Returns (pivot_indices, transformed_matrix, transformed_augmented_col)
    """
    m = len(matrix)
    if m == 0: return [], [], []
    n = len(matrix[0])
    mat = [row[:] for row in matrix]
    col = augmented_col[:] if augmented_col else None
    
    pivot_indices = []
    curr_row = 0
    
    for c in range(n):
        if curr_row >= m:
            break
            
        # Find pivot
        pivot_row = -1
        for r in range(curr_row, m):
            if mat[r][c] == 1:
                pivot_row = r
                break
        
        if pivot_row == -1:
            continue
            
        # Swap rows
        mat[curr_row], mat[pivot_row] = mat[pivot_row], mat[curr_row]
        if col:
            col[curr_row], col[pivot_row] = col[pivot_row], col[curr_row]
            
        pivot_indices.append(c)
        
        # Eliminate other rows
        for r in range(m):
            if r != curr_row and mat[r][c] == 1:
                # Row XOR
                for k in range(c, n):
                    mat[r][k] ^= mat[curr_row][k]
                if col:
                    col[r] ^= col[curr_row]
        
        curr_row += 1
        
    return pivot_indices, mat, col

def solve_machine_part1(target, buttons):
    """
    Solves Ax = b over GF(2) minimizing Hamming weight.
    """
    if not buttons:
        return 0 if all(t == 0 for t in target) else float('inf')
        
    num_items = len(target)
    num_buttons = len(buttons)
    
    # Construct Matrix A (rows = items, cols = buttons)
    A = [[buttons[j][i] for j in range(num_buttons)] for i in range(num_items)]
    
    # RREF augmented
    pivots, rref_A, rref_b = rref_gf2(A, target)
    
    # Check consistency
    for r in range(num_items):
        if all(val == 0 for val in rref_A[r]) and rref_b[r] == 1:
            return float('inf')
            
    # Find free variables
    pivot_set = set(pivots)
    free_vars = [j for j in range(num_buttons) if j not in pivot_set]
    
    # Particular solution
    x_p = [0] * num_buttons
    for r, c in enumerate(pivots):
        x_p[c] = rref_b[r]
        
    if not free_vars:
        return sum(x_p)
        
    # Null space basis
    null_basis = []
    for f in free_vars:
        v = [0] * num_buttons
        v[f] = 1
        for r, c in enumerate(pivots):
            if rref_A[r][f] == 1:
                v[c] = 1
        null_basis.append(v)
        
    # Brute force free variables (assuming num free vars is small)
    min_weight = float('inf')
    
    import itertools
    for coeffs in itertools.product([0, 1], repeat=len(free_vars)):
        current_x = list(x_p)
        for i, coeff in enumerate(coeffs):
            if coeff == 1:
                for j in range(num_buttons):
                    current_x[j] ^= null_basis[i][j]
        
        weight = sum(current_x)
        if weight < min_weight:
            min_weight = weight
            
    return min_weight

try:
    from z3 import Optimize, Int, sat, Sum
except ImportError:
    Optimize = None

def solve_machine_part2(target, buttons):
    """
    Solves Ax = b over Integers (non-negative) minimizing sum(x) using Z3.
    """
    if Optimize is None:
        return "Z3 not installed"
        
    num_items = len(target)
    num_buttons = len(buttons)
    
    opt = Optimize()
    presses = [Int(f'p_{i}') for i in range(num_buttons)]
    
    # Non-negative constraints
    for p in presses:
        opt.add(p >= 0)
        
    # Equation constraints
    # target[i] = sum(buttons[j][i] * presses[j])
    for i in range(num_items):
        equation = Sum([buttons[j][i] * presses[j] for j in range(num_buttons)]) == target[i]
        opt.add(equation)
        
    # Minimize total presses
    total_presses = Sum(presses)
    opt.minimize(total_presses)
    
    if opt.check() == sat:
        model = opt.model()
        min_presses = model.eval(total_presses).as_long()
        return min_presses
    else:
        return float('inf')

def part1(data):
    # data is already parsed by main.py if parse function exists
    machines = data if isinstance(data, list) else parse(data)
    total_presses = 0
    for target, buttons, _ in machines:
        presses = solve_machine_part1(target, buttons)
        if presses != float('inf'):
            total_presses += presses
    return total_presses

def part2(data):
    machines = data if isinstance(data, list) else parse(data)
    total_presses = 0
    for i, (_, buttons, joltage) in enumerate(machines):
        presses = solve_machine_part2(joltage, buttons)
        if presses == float('inf'):
            print(f"Machine {i} has no solution for Part 2")
            return "No solution found"
        total_presses += presses
    return total_presses
