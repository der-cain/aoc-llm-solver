from src.year2025.day05 import parse, part1

example_input = """3-5 10-14 16-20 12-18

1 5 8 11 17 32"""

parsed = parse(example_input)
result = part1(parsed)

print(f"Example Result: {result}")
expected = 3
assert result == expected, f"Expected {expected}, got {result}"
print("Test Passed!")
