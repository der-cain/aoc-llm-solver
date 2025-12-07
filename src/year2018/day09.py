from collections import deque
import re

def parse(data):
    """
    Parses the input string to extract number of players and last marble value.
    Example input: "10 players; last marble is worth 1618 points"
    """
    match = re.search(r"(\d+) players; last marble is worth (\d+) points", data)
    if match:
        return int(match.group(1)), int(match.group(2))
    raise ValueError("Invalid input format")

def solve_game(players, last_marble):
    """
    Simulates the marble game and returns the highest score.
    """
    scores = [0] * players
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            current_player = (marble - 1) % players
            scores[current_player] += marble
            circle.rotate(7)
            scores[current_player] += circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)

def part1(data):
    players, last_marble = data
    return solve_game(players, last_marble)

def part2(data):
    players, last_marble = data
    return solve_game(players, last_marble * 100)
