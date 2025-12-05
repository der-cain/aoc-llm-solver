from src.year2025.day01 import parse, part1

example_input = "L68 L30 R48 L5 R60 L55 L1 L99 R14 L82"
parsed = parse(example_input)
result = part1(parsed)

print(f"Example Result: {result}")
assert result == 3, f"Expected 3, got {result}"
print("Test Passed!")
