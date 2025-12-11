from src.year2025.day11 import part1, parse

EXAMPLE_INPUT = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

def test_example_part1():
    graph = parse(EXAMPLE_INPUT)
    assert part1(graph) == 5

def test_parse_input():
    graph = parse(EXAMPLE_INPUT)
    assert 'you' in graph
    assert set(graph['you']) == {'bbb', 'ccc'}
    assert 'iii' in graph
    assert graph['iii'] == ['out']

EXAMPLE_INPUT_2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

def test_example_part2():
    graph = parse(EXAMPLE_INPUT_2)
    # The example says "How many of those paths visit both dac and fft?" -> 2
    from src.year2025.day11 import part2
    assert part2(graph) == 2

