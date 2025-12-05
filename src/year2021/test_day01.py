from src.year2021.day01 import parse, part1, part2

example_input = """199
200
208
210
200
207
240
269
260
263"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 7, f"Expected 7, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 5, f"Expected 5, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

