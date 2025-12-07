from src.year2021.day07 import parse, part1, part2

example_input = """16,1,2,0,4,2,7,1,2,14"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 37, f"Expected 37, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 168, f"Expected 168, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

