from src.year2021.day17 import parse, part1, part2

example_input = "target area: x=20..30, y=-10..-5"

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 45, f"Expected 45, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 112, f"Expected 112, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

