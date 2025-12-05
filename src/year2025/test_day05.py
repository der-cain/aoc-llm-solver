from src.year2025.day05 import parse, part1, part2

example_input = """3-5 10-14 16-20 12-18

1 5 8 11 17 32"""

parsed = parse(example_input)
result = part1(parsed)

result = part1(parsed)
print(f"Part 1 Result: {result}")
expected = 3
assert result == expected, f"Expected {expected}, got {result}"

result2 = part2(parsed)
print(f"Part 2 Result: {result2}")
expected2 = 14
assert result2 == expected2, f"Expected {expected2}, got {result2}"

print("Test Passed!")
