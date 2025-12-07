# Copied opcodes from Day 16
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

def run(ip_reg, program, r0=0):
    regs = [0] * 6
    regs[0] = r0
    ip = 0

    while 0 <= ip < len(program):
        regs[ip_reg] = ip
        op_name, (a, b, c) = program[ip]
        regs[c] = OPS[op_name](regs, a, b)
        ip = regs[ip_reg]
        ip += 1

    return regs[0]

def part1(data):
    ip_reg, program = data
    return run(ip_reg, program)

def part2(data):
    # Part 2 usually involves a long running loop.
    # The program likely calculates sum of divisors.

    ip_reg, program = data

    regs = [0] * 6
    regs[0] = 1 # Part 2 start
    ip = 0

    # Run for a bit to let it initialize the target number
    max_steps = 1000
    target_candidate = 0

    for _ in range(max_steps):
        if not (0 <= ip < len(program)):
            break
        regs[ip_reg] = ip
        op_name, (a, b, c) = program[ip]
        regs[c] = OPS[op_name](regs, a, b)
        ip = regs[ip_reg]
        ip += 1

        # Check for large number in registers
        # Usually target is much larger than typical loop counters
        if max(regs) > 1000000:
            target_candidate = max(regs)
            # We found a large number. Assuming this is the target.
            # We can break early?
            # The initialization might take more steps, but once it sets the large number, it enters the main loop.
            # Let's run a bit more to ensure it's stable.
            pass

    if target_candidate > 0:
        # Calculate sum of divisors
        total = 0
        for i in range(1, int(target_candidate**0.5) + 1):
            if target_candidate % i == 0:
                total += i
                if i * i != target_candidate:
                    total += target_candidate // i
        return total

    return "Could not determine target"
