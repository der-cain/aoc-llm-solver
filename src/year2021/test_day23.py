from src.year2021.day23 import parse, part1, part2

example_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 12521, f"Expected 12521, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 44169, f"Expected 44169, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

