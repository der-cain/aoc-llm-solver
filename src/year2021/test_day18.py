from src.year2021.day18 import parse, part1, part2

example_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

def test_part1():
    # We must ensure that parse returns fresh objects for each call if we're not careful, 
    # but here parse returns a list of objects. Part 1 consumes them.
    parsed = parse(example_input)
    result = part1(parsed)
    print(f"Part 1 Example Result: {result}")
    assert result == 4140, f"Expected 4140, got {result}"

def test_part2():
    parsed = parse(example_input)
    result = part2(parsed)
    print(f"Part 2 Example Result: {result}")
    assert result == 3993, f"Expected 3993, got {result}"

def test_reduction():
    # Test case from problem description
    from src.year2021.day18 import parse_flat, reduce_flat
    
    start_str = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    
    # Parse flat
    flat = parse_flat(start_str)
    
    # Reduce
    reduce_flat(flat)
    
    # Convert back to tree string or list for comparison?
    # Or just check magnitude?
    # Or check flat structure.
    # Expected: [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    # Flat expected:
    expected_str = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    expected_flat = parse_flat(expected_str)
    
    print(f"Result Flat: {flat}")
    print(f"Expect Flat: {expected_flat}")
    
    assert flat == expected_flat, "Reduction failed"

def test_magnitude():
    from src.year2021.day18 import parse_flat, magnitude_flat
    
    examples = [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)
    ]
    
    for s, expected in examples:
        flat = parse_flat(s)
        mag = magnitude_flat(flat)
        print(f"Magnitude of {s[:20]}...: {mag} (Expected {expected})")
        assert mag == expected, f"Expected {expected}, got {mag}"


if __name__ == "__main__":
    test_part1()
    test_part2()
    test_reduction()
    test_magnitude()
    print("Test Passed!")



