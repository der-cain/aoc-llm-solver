from src.year2021.day02 import parse, part1, part2

example_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 150, f"Expected 150, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 900, f"Expected 900, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

