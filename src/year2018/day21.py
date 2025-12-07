# Copied opcodes from Day 19
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

OPS = {
    'addr': addr, 'addi': addi, 'mulr': mulr, 'muli': muli,
    'banr': banr, 'bani': bani, 'borr': borr, 'bori': bori,
    'setr': setr, 'seti': seti, 'gtir': gtir, 'gtri': gtri,
    'gtrr': gtrr, 'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr
}

def parse(data):
    lines = data.strip().split('\n')
    ip_reg = int(lines[0].split()[1])
    program = []
    for line in lines[1:]:
        parts = line.split()
        op = parts[0]
        args = list(map(int, parts[1:]))
        program.append((op, args))
    return ip_reg, program

def solve_optimized(program):
    # This logic mimics the input program.
    # We should dynamically extract constants if possible, or assume the structure matches.
    # The constants are:
    # Instr 6: bori 5 65536 3 -> 65536
    # Instr 7: seti 733884 6 5 -> 733884
    # Instr 11: muli 5 65899 5 -> 65899
    # The logic is fixed otherwise.

    # Extract constants
    try:
        c1 = program[6][1][1] # 65536
        c2 = program[7][1][0] # 733884
        c3 = program[11][1][1] # 65899
    except IndexError:
        # Fallback to hardcoded if program structure differs significantly
        return None, None

    r5 = 0
    seen = set()
    last_unique = None
    first_r5 = None

    while True:
        r3 = r5 | c1
        r5 = c2

        while True:
            r1 = r3 & 255
            r5 = r5 + r1
            r5 = r5 & 16777215
            r5 = r5 * c3
            r5 = r5 & 16777215

            if 256 > r3:
                # Check point
                if first_r5 is None:
                    first_r5 = r5

                if r5 in seen:
                    return first_r5, last_unique

                seen.add(r5)
                last_unique = r5
                break
            else:
                r3 = r3 // 256

def part1(data):
    ip_reg, program = data
    # Check if we can use optimized solution
    res = solve_optimized(program)
    if res and res[0] is not None:
        return res[0]

    # Fallback to simulation (slow)
    return "Optimization failed"

def part2(data):
    ip_reg, program = data
    res = solve_optimized(program)
    if res and res[1] is not None:
        return res[1]
    return "Optimization failed"
