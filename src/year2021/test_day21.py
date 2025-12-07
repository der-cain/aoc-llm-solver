from src.year2021.day21 import parse, part1, part2

example_input = """Player 1 starting position: 4
Player 2 starting position: 8"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 739785, f"Expected 739785, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 444356092776315, f"Expected 444356092776315, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

