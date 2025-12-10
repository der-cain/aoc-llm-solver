
import pytest
from src.year2025.day10 import parse, part1, part2, solve_machine_part1, solve_machine_part2

EXAMPLE_INPUT = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()

def test_parse():
    machines = parse(EXAMPLE_INPUT)
    assert len(machines) == 3
    
    # Check first machine
    target, buttons, joltage = machines[0]
    assert target == [0, 1, 1, 0]
    assert joltage == [3, 5, 4, 7]
    
    assert buttons[0] == [0, 0, 0, 1]

def test_solve_machine_part1():
    machines = parse(EXAMPLE_INPUT)
    target, buttons, _ = machines[0]
    min_presses = solve_machine_part1(target, buttons)
    assert min_presses == 2

def test_solve_machine_part2_1():
    machines = parse(EXAMPLE_INPUT)
    _, buttons, joltage = machines[0]
    min_presses = solve_machine_part2(joltage, buttons)
    assert min_presses == 10

def test_solve_machine_part2_2():
    machines = parse(EXAMPLE_INPUT)
    _, buttons, joltage = machines[1]
    min_presses = solve_machine_part2(joltage, buttons)
    assert min_presses == 12

def test_solve_machine_part2_3():
    machines = parse(EXAMPLE_INPUT)
    _, buttons, joltage = machines[2]
    min_presses = solve_machine_part2(joltage, buttons)
    assert min_presses == 11

def test_part1():
    result = part1(EXAMPLE_INPUT)
    assert result == 7

def test_part2():
    result = part2(EXAMPLE_INPUT)
    assert result == 33
