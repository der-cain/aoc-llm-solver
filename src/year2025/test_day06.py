from src.year2025.day06 import parse, part1, part2

# Exact copy from description
example_input_v2 = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

def test_part1():
    parsed = parse(example_input_v2)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 4277556, f"Expected 4277556, got {result}"

def test_part2():
    parsed = parse(example_input_v2)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 3263827, f"Expected 3263827, got {result}"


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

