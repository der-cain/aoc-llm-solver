from src.year2021.day03 import parse, part1, part2

example_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 198, f"Expected 198, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 230, f"Expected 230, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

