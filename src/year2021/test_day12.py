from src.year2021.day12 import parse, part1, part2

example_input_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

example_input_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

example_input_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

def test_part1():
    parsed1 = parse(example_input_1)
    result1 = part1(parsed1)
    print(f"Part 1 Example 1 Result: {result1}")
    assert result1 == 10, f"Expected 10, got {result1}"

    parsed2 = parse(example_input_2)
    result2 = part1(parsed2)
    print(f"Part 1 Example 2 Result: {result2}")
    assert result2 == 19, f"Expected 19, got {result2}"
    
    parsed3 = parse(example_input_3)
    result3 = part1(parsed3)
    print(f"Part 1 Example 3 Result: {result3}")
    assert result3 == 226, f"Expected 226, got {result3}"

def test_part2():
    parsed1 = parse(example_input_1)
    result1 = part2(parsed1)
    print(f"Part 2 Example 1 Result: {result1}")
    assert result1 == 36, f"Expected 36, got {result1}"

    parsed2 = parse(example_input_2)
    result2 = part2(parsed2)
    print(f"Part 2 Example 2 Result: {result2}")
    assert result2 == 103, f"Expected 103, got {result2}"
    
    parsed3 = parse(example_input_3)
    result3 = part2(parsed3)
    print(f"Part 2 Example 3 Result: {result3}")
    assert result3 == 3509, f"Expected 3509, got {result3}"

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

