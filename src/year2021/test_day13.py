from src.year2021.day13 import parse, part1, part2

example_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 17, f"Expected 17, got {result}"

def test_part2():
    parsed = parse(example_input)
    # Part 2 returns a grid string for the example, which forms a square.
    # The example says "The instructions made a square!"
    # x=5 fold -> width 5.
    # y=7 fold -> height 7? No, previous fold was y=7.
    # Actually let's just inspect the output.
    result = part2(parsed)
    # Expected square of '#'
    expected = "#####\n#...#\n#...#\n#...#\n#####"
    # Note: my implementation uses spaces for '.'
    # Update expectation to match spaces
    expected_spaces = "#####\n#   #\n#   #\n#   #\n#####"
    print("Part 2 Example Result Grid:")
    print(result)
    assert result.strip() == expected_spaces.strip()

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

