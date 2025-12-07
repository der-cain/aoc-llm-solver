from src.year2021.day14 import parse, part1, part2

example_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def test_part1():
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 1588, f"Expected 1588, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 2188189693529, f"Expected 2188189693529, got {result}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

