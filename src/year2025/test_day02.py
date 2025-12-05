from src.year2025.day02 import parse, part1, part2

example_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224, 1698522-1698528,446443-446449,38593856-38593862,565653-565659, 824824821-824824827,2121212118-2121212124"
parsed = parse(example_input)
result = part1(parsed)
print(f"Part 1 Result: {result}")
expected = 1227775554
assert result == expected, f"Expected {expected}, got {result}"

result2 = part2(parsed)
print(f"Part 2 Result: {result2}")
expected2 = 4174379265
assert result2 == expected2, f"Expected {expected2}, got {result2}"

print("Test Passed!")
