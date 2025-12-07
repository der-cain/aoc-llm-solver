from src.year2021.day25 import parse, part1

example_input = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 58, f"Expected 58, got {result}"

if __name__ == "__main__":
    test_part1()
    print("Test Passed!")
