from src.year2021.day09 import parse, part1, part2

example_input = """2199943210
3987894921
9856789892
8767896789
9899965678"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 15, f"Expected 15, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 1134, f"Expected 1134, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

