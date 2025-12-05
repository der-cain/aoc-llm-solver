from src.year2025.day03 import parse, part1, part2

example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""

parsed = parse(example_input)
result = part1(parsed)
print(f"Part 1 Result: {result}")
expected = 357
assert result == expected, f"Expected {expected}, got {result}"

result2 = part2(parsed)
print(f"Part 2 Result: {result2}")
expected2 = 3121910778619
assert result2 == expected2, f"Expected {expected2}, got {result2}"

print("Test Passed!")
