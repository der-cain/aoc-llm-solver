def solve_part1(num_recipes):
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    while len(recipes) < num_recipes + 10:
        score1 = recipes[elf1]
        score2 = recipes[elf2]
        total = score1 + score2

        if total >= 10:
            recipes.append(total // 10)
            recipes.append(total % 10)
        else:
            recipes.append(total)

        elf1 = (elf1 + 1 + score1) % len(recipes)
        elf2 = (elf2 + 1 + score2) % len(recipes)

    return ''.join(map(str, recipes[num_recipes:num_recipes+10]))

def solve_part2(target_seq_str):
    target_seq = [int(c) for c in target_seq_str]
    target_len = len(target_seq)

    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    # We check for the sequence at the end of recipes list
    # Since we can add 1 or 2 recipes per turn, we check last `target_len` and `target_len+1`

    while True:
        score1 = recipes[elf1]
        score2 = recipes[elf2]
        total = score1 + score2

        digits = []
        if total >= 10:
            digits = [total // 10, total % 10]
        else:
            digits = [total]

        for d in digits:
            recipes.append(d)
            if len(recipes) >= target_len:
                # Check if suffix matches
                # Optimization: check last added digit first?
                # Actually, slicing is fast enough for small target_len (6 digits usually)
                if recipes[-target_len:] == target_seq:
                    return len(recipes) - target_len

        elf1 = (elf1 + 1 + score1) % len(recipes)
        elf2 = (elf2 + 1 + score2) % len(recipes)

def part1(data):
    return solve_part1(int(data))

def part2(data):
    return solve_part2(data.strip())
