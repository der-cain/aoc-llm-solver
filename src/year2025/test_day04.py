from src.year2025.day04 import parse, part1

example_input = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
parsed = parse(example_input)
result = part1(parsed)

print(f"Example Result: {result}")
expected = 13
assert result == expected, f"Expected {expected}, got {result}"
print("Test Passed!")
