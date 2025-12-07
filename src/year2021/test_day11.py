from src.year2021.day11 import parse, part1, part2

example_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 1656, f"Expected 1656, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 195, f"Expected 195, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

