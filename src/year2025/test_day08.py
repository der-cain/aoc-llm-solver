import unittest
from src.year2025.day08 import part1, part2

class TestDay08(unittest.TestCase):
    def setUp(self):
        self.example_data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

    def test_part1_example(self):
        from src.year2025.day08 import parse
        self.assertEqual(part1(parse(self.example_data)), 40)

    def test_part2_example(self):
        from src.year2025.day08 import parse
        self.assertEqual(part2(parse(self.example_data)), 25272)
