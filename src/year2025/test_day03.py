from src.year2025.day03 import parse, part1

example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""

parsed = parse(example_input)
result = part1(parsed)

print(f"Example Result: {result}")
expected = 357
assert result == expected, f"Expected {expected}, got {result}"
print("Test Passed!")
