def parse(data):
    lines = data.strip().splitlines()
    p1 = int(lines[0].split(": ")[1])
    p2 = int(lines[1].split(": ")[1])
    return p1, p2

def part1(parsed_data):
    p1_pos, p2_pos = parsed_data
    p1_score = 0
    p2_score = 0
    
    die_val = 1
    total_rolls = 0
    
    while True:
        # Player 1
        move = 0
        for _ in range(3):
            move += die_val
            die_val += 1
            if die_val > 100:
                die_val = 1
            total_rolls += 1
            
        p1_pos = (p1_pos + move - 1) % 10 + 1
        p1_score += p1_pos
        
        if p1_score >= 1000:
            return p2_score * total_rolls
            
        # Player 2
        move = 0
        for _ in range(3):
            move += die_val
            die_val += 1
            if die_val > 100:
                die_val = 1
            total_rolls += 1
            
        p2_pos = (p2_pos + move - 1) % 10 + 1
        p2_score += p2_pos
        
        if p2_score >= 1000:
            return p1_score * total_rolls

from functools import lru_cache

def part2(parsed_data):
    start_p1, start_p2 = parsed_data
    
    # Outcomes of 3 rolls of 3-sided die
    # 1,1,1 = 3 (1 way)
    # 1,1,2 = 4 (3 ways)
    # 1,2,2 = 5 (3 ways)
    # 2,2,2 = 6 (1 way)... wait, calculate frequencies
    # 3 rolls of {1,2,3}
    # Sums range from 3 to 9.
    
    # 3: 1+1+1 (1)
    # 4: 1+1+2, 1+2+1, 2+1+1 (3)
    # 5: 1+1+3, 1+3+1, 3+1+1, 1+2+2, 2+1+2, 2+2+1 (6)
    # 6: 1+2+3 (6 perms), 2+2+2 (1), ... 
    # Let's just generate them or hardcode map.
    roll_distribution = {
        3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1
    }
    
    @lru_cache(maxsize=None)
    def count_universes(p1, p2, score1, score2, turn_p1=True):
        if score1 >= 21:
            return 1, 0
        if score2 >= 21:
            return 0, 1
            
        wins1, wins2 = 0, 0
        
        for roll, freq in roll_distribution.items():
            if turn_p1:
                new_p1 = (p1 + roll - 1) % 10 + 1
                new_s1 = score1 + new_p1
                w1, w2 = count_universes(new_p1, p2, new_s1, score2, False)
            else:
                new_p2 = (p2 + roll - 1) % 10 + 1
                new_s2 = score2 + new_p2
                w1, w2 = count_universes(p1, new_p2, score1, new_s2, True)
            
            wins1 += w1 * freq
            wins2 += w2 * freq
            
        return wins1, wins2

    w1, w2 = count_universes(start_p1, start_p2, 0, 0, True)
    return max(w1, w2)

