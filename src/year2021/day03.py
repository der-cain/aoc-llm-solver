def parse(data):
    return [line.strip() for line in data.splitlines() if line.strip()]

def part1(data):
    # Determine length of binary numbers
    if not data:
        return 0
    
    length = len(data[0])
    total_count = len(data)
    
    gamma_bits = []
    epsilon_bits = []
    
    for i in range(length):
        ones_count = sum(1 for line in data if line[i] == '1')
        zeros_count = total_count - ones_count
        
        if ones_count > zeros_count:
            gamma_bits.append('1')
            epsilon_bits.append('0')
        else:
            gamma_bits.append('0')
            epsilon_bits.append('1')
            
    gamma = int("".join(gamma_bits), 2)
    epsilon = int("".join(epsilon_bits), 2)
    
    return gamma * epsilon

def get_rating(data, criteria_func):
    remaining = data[:]
    bit_index = 0
    while len(remaining) > 1:
        ones = sum(1 for line in remaining if line[bit_index] == '1')
        zeros = len(remaining) - ones
        
        target_bit = criteria_func(ones, zeros)
        remaining = [line for line in remaining if line[bit_index] == target_bit]
        bit_index += 1
        
    return int(remaining[0], 2)

def part2(data):
    oxygen = get_rating(data, lambda ones, zeros: '1' if ones >= zeros else '0')
    co2 = get_rating(data, lambda ones, zeros: '0' if zeros <= ones else '1')
    
    return oxygen * co2
