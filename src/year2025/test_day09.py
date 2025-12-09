import unittest
from src.year2025.day09 import parse, part1, part2

class TestDay09(unittest.TestCase):
    def test_part1(self):
        input_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
        data = parse(input_data)
        self.assertEqual(part1(data), 50)

    def test_part2(self):
        input_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
        data = parse(input_data)
        self.assertEqual(part2(data), 24)

if __name__ == '__main__':
    unittest.main()
