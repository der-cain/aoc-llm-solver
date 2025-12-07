from src.year2021.day10 import parse, part1, part2

example_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 26397, f"Expected 26397, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 288957, f"Expected 288957, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

