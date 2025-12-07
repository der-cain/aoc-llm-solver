import re

def parse_input(data):
    samples = []
    program = []

    parts = data.split('\n\n\n')

    sample_part = parts[0]
    program_part = parts[1] if len(parts) > 1 else ""

    # Parse samples
    sample_lines = sample_part.split('\n')
    i = 0
    while i < len(sample_lines):
        line = sample_lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith('Before:'):
            before = list(map(int, re.findall(r'\d+', line)))
            instr = list(map(int, re.findall(r'\d+', sample_lines[i+1])))
            after = list(map(int, re.findall(r'\d+', sample_lines[i+2])))
            samples.append({
                'before': before,
                'instr': instr,
                'after': after
            })
            i += 3
        else:
            i += 1

    # Parse program
    if program_part:
        for line in program_part.split('\n'):
            line = line.strip()
            if line:
                program.append(list(map(int, re.findall(r'\d+', line))))

    return samples, program

# Operations
def addr(regs, a, b): return regs[a] + regs[b]
def addi(regs, a, b): return regs[a] + b
def mulr(regs, a, b): return regs[a] * regs[b]
def muli(regs, a, b): return regs[a] * b
def banr(regs, a, b): return regs[a] & regs[b]
def bani(regs, a, b): return regs[a] & b
def borr(regs, a, b): return regs[a] | regs[b]
def bori(regs, a, b): return regs[a] | b
def setr(regs, a, b): return regs[a]
def seti(regs, a, b): return a
def gtir(regs, a, b): return 1 if a > regs[b] else 0
def gtri(regs, a, b): return 1 if regs[a] > b else 0
def gtrr(regs, a, b): return 1 if regs[a] > regs[b] else 0
def eqir(regs, a, b): return 1 if a == regs[b] else 0
def eqri(regs, a, b): return 1 if regs[a] == b else 0
def eqrr(regs, a, b): return 1 if regs[a] == regs[b] else 0

ALL_OPS = [
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
]

def check_sample(sample):
    matches = 0
    possible_ops = set()

    before = sample['before']
    instr = sample['instr']
    after = sample['after']

    op_code, a, b, c = instr

    for op in ALL_OPS:
        # Check if op matches behavior
        regs = list(before)
        try:
            res = op(regs, a, b)
            regs[c] = res
            if regs == after:
                matches += 1
                possible_ops.add(op.__name__)
        except IndexError:
            pass

    return matches, possible_ops

def part1(data):
    samples, _ = parse_input(data)
    count = 0
    for s in samples:
        matches, _ = check_sample(s)
        if matches >= 3:
            count += 1
    return count

def part2(data):
    samples, program = parse_input(data)

    # Deduce opcodes
    opcode_map = {i: set(op.__name__ for op in ALL_OPS) for i in range(16)}

    for s in samples:
        op_code = s['instr'][0]
        _, possible = check_sample(s)
        opcode_map[op_code] &= possible

    # Simplify map (constraint propagation)
    final_map = {}
    while len(final_map) < 16:
        # Find opcodes with only 1 possibility
        for code, possible in opcode_map.items():
            if code not in final_map and len(possible) == 1:
                op_name = list(possible)[0]
                final_map[code] = op_name

                # Remove this op_name from all others
                for other_code in opcode_map:
                    if other_code != code:
                        opcode_map[other_code].discard(op_name)

    # Map back to functions
    name_to_func = {op.__name__: op for op in ALL_OPS}
    final_func_map = {code: name_to_func[name] for code, name in final_map.items()}

    # Run program
    regs = [0, 0, 0, 0]
    for instr in program:
        op_code, a, b, c = instr
        op = final_func_map[op_code]
        regs[c] = op(regs, a, b)

    return regs[0]
