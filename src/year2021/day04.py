class Board:
    def __init__(self, rows):
        self.rows = rows
        self.cols = list(zip(*rows))
        self.marked = set()
        self.all_nums = {num for row in rows for num in row}
        
    def mark(self, num):
        if num in self.all_nums:
            self.marked.add(num)
            
    def is_winner(self):
        # Check rows
        for row in self.rows:
            if all(num in self.marked for num in row):
                return True
        # Check cols
        for col in self.cols:
            if all(num in self.marked for num in col):
                return True
        return False
        
    def score(self, last_called):
        unmarked_sum = sum(num for num in self.all_nums if num not in self.marked)
        return unmarked_sum * last_called


def parse(data):
    lines = [line.strip() for line in data.splitlines()]
    draws = [int(x) for x in lines[0].split(',')]
    
    boards = []
    current_board_rows = []
    
    for line in lines[1:]:
        if not line:
            if current_board_rows:
                boards.append(Board(current_board_rows))
                current_board_rows = []
        else:
            current_board_rows.append([int(x) for x in line.split()])
            
    if current_board_rows:
        boards.append(Board(current_board_rows))
        
    return draws, boards

def part2(parsed_data):
    draws, boards = parsed_data
    # Reset boards because part1 marked them
    # But parsed_data is passed twice? 
    # Actually wait, `main.py` calls parse once for both parts usually?
    # Wait, `main.py` calls `parse(data)` then passes `parsed_data` to `part1` and `part2`.
    # BUT `part1` modified the boards in-place (marked them).
    # So `part2` will receive already marked boards!
    # I need to re-parse or copy or reset.
    # Since I cannot easily re-parse here without raw data, I should probably assume `part1` and `part2` might share state issues if I don't handle it.
    
    # However, `main.py` code:
    # parsed = module.parse(data)
    # result1 = module.part1(parsed)
    # result2 = module.part2(parsed)
    
    # My `part1` implementation modified `boards`.
    # I should modify `part1` to work on a COPY or `part2` to reset?
    # Or easier: modify `parse` to return fresh objects? No, `parse` is called once.
    # I will modify `part1` and `part2` to deepcopy the boards if necessary, or just reset them.
    # But `Board` class doesn't have reset.
    # I'll just clear `marked` set in `part2`? No, I don't know what `part1` marked.
    
    # Better approach: Modify `part1` to NOT modify the passed boards?
    # Or implement a `reset` method.
    # Or, in `part2`, I can assume `part1` already marked some?
    # No, `part1` returns when *first* wins, but leaves others marked.
    
    # Actually, `part2` needs to simulate from start to find last winner.
    # If I receive partially marked boards, `part2` logic is flawed.
    
    # I will update `parse` to return a structure that can be deepcopied, or just deepcopy in parts.
    import copy
    draws_copy = copy.deepcopy(draws)
    boards_copy = copy.deepcopy(boards)
    
    # Wait, if `part1` was called first, `boards` in `parsed_data` are dirty.
    # I should have `part1` use a copy.
    # I will fix `part1` to use a copy, and `part2` to use a copy.
    # But I can only edit `day04.py`.
    # I will edit `part1` to copy inputs.
    pass

def part1(parsed_data):
    import copy
    draws, boards_orig = parsed_data
    boards = copy.deepcopy(boards_orig)
    
    for draw in draws:
        for board in boards:
            board.mark(draw)
            if board.is_winner():
                return board.score(draw)
                
    return 0

def part2(parsed_data):
    import copy
    draws, boards_orig = parsed_data
    boards = copy.deepcopy(boards_orig)
    
    total_boards = len(boards)
    won_boards = set()
    
    for draw in draws:
        for i, board in enumerate(boards):
            if i in won_boards:
                continue
                
            board.mark(draw)
            if board.is_winner():
                won_boards.add(i)
                if len(won_boards) == total_boards:
                    return board.score(draw)
    return 0
