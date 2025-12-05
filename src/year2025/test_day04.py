from src.year2025.day04 import parse, part1, part2

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
print(f"Part 1 Result: {result}")
expected = 13
assert result == expected, f"Expected {expected}, got {result}"

result2 = part2(parsed)
print(f"Part 2 Result: {result2}")
expected2 = 43
assert result2 == expected2, f"Expected {expected2}, got {result2}"

print("Test Passed!")
