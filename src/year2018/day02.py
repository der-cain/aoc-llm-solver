from collections import Counter

def parse(data):
    return data.splitlines()

def part1(data):
    two_count = 0
    three_count = 0
    for box_id in data:
        counts = Counter(box_id).values()
        if 2 in counts:
            two_count += 1
        if 3 in counts:
            three_count += 1
    return two_count * three_count

def part2(data):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            s1 = data[i]
            s2 = data[j]
            diff = 0
            diff_index = -1
            for k, (c1, c2) in enumerate(zip(s1, s2)):
                if c1 != c2:
                    diff += 1
                    diff_index = k
                    if diff > 1:
                        break
            if diff == 1:
                return s1[:diff_index] + s1[diff_index+1:]
