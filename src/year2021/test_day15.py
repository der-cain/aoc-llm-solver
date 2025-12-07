from src.year2021.day15 import parse, part1, part2

example_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 40, f"Expected 40, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 315, f"Expected 315, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

