import unittest
from src.year2018.day09 import solve_game, parse

class TestDay09(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse("10 players; last marble is worth 1618 points"), (10, 1618))

    def test_solve_game_examples(self):
        self.assertEqual(solve_game(9, 25), 32)
        self.assertEqual(solve_game(10, 1618), 8317)
        self.assertEqual(solve_game(13, 7999), 146373)
        self.assertEqual(solve_game(17, 1104), 2764)
        self.assertEqual(solve_game(21, 6111), 54718)
        self.assertEqual(solve_game(30, 5807), 37305)

if __name__ == '__main__':
    unittest.main()
