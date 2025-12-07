from src.year2021.day06 import parse, part1, part2

example_input = """3,4,3,1,2"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 5934, f"Expected 5934, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 26984457539, f"Expected 26984457539, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

