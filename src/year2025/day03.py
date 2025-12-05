def parse(input_data):
    # Split into lines
    return input_data.strip().split()

def solve_line(line):
    max_val = 0
    # Try all pairs of indices (i, j) with i < j
    # This is O(N^2), suitable for typical AoC line lengths.
    for i in range(len(line)):
        for j in range(i + 1, len(line)):
            val = int(line[i] + line[j])
            if val > max_val:
                max_val = val
    return max_val

def part1(data):
    total = 0
    for line in data:
        line = line.strip()
        if not line:
            continue
        total += solve_line(line)
    return total

def part2(data):
    total = 0
    k = 12
    for line in data:
        line = line.strip()
        if not line:
            continue
        
        # Find subsequence of length k with max numeric value
        # Greedy approach: pick largest available digit for each position
        
        n = len(line)
        if n < k:
             # Should not happen based on problem statement, but safety
             continue
             
        current_idx = 0
        result_digits = []
        
        for i in range(k):
            # We need to pick total k digits. We have picked i so far.
            # We need to pick k - i digits (including this one).
            # So we must leave (k - i - 1) digits after this choice.
            remaining_needed = k - i - 1
            max_search_idx = n - remaining_needed
            
            # Search window
            window = line[current_idx : max_search_idx]
            
            # Find max digit - since they are digits 0-9, standard string comparison works
            # '9' > '8' etc.
            best_digit = max(window)
            
            # Find FIRST occurrence of best_digit to leave most room
            # window.index finds first occurrence
            offset = window.index(best_digit)
            actual_idx = current_idx + offset
            
            result_digits.append(best_digit)
            current_idx = actual_idx + 1
            
        total += int("".join(result_digits))
        
    return total
