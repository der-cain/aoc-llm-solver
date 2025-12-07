from src.year2021.day24 import parse, part1

# We can't easily test this with full logic without real input because expected output isn't known for sub-chunks.
# But we can verify it doesn't crash on standard input structure.

example_input = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2""" # This example from description doesn't match MONAD structure.

# Let's create a fake MONAD-like structure for testing basic parsing/extraction
fake_monad = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
""" * 14

def test_parsing():
    parsed = parse(fake_monad)
    assert len(parsed) == 14
    print("Parsing successful")

if __name__ == "__main__":
    test_parsing()
    print("Test Passed!")
