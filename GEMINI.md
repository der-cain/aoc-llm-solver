# Advent of Code Solver Instructions for Agent

## 1. Authentication (AOC_SESSION)
**CRITICAL**: You need a valid session cookie to fetch specific user inputs and submit answers.
- Ensure `AOC_SESSION` is present in the `.env` file.
- If missing, ask the user to provide it.

## 2. Puzzle Progress Flow
Advent of Code puzzles are unlocked sequentially.
> [!IMPORTANT]
> **Part 2 of a puzzle is HIDDEN** until Part 1 is successfully solved and submitted.

### Step 1: Read Problem Description
- **Standardized Method**: Use the `fetch_puzzle.py` script. This handles authentication and fetching both parts (if available).
  ```bash
  python fetch_puzzle.py --year <YEAR> --day <DAY> --output day<DAY>_desc.html
  ```
- **Read Output**: Use `view_file` to read the generated HTML file.
- **Failover**: If the script fails, fallback to `read_url_content` (note: Part 2 might be hidden).

### Step 2: Fetch Input
- **Python**: Use `from src.utils import get_input`.
- **Do NOT** read input from the website text. Always use the `get_input` function which caches it to `inputs/`.

### Step 3: Implementation & Testing
The puzzles usually contain testing data which you can use to validate your solution.
- Create a new file `src/year<YEAR>/day<DAY>.py`.
- Create a corresponding test file `src/year<YEAR>/test_day<DAY>.py`.
- **Testing**: Run pytest:
  ```bash
  python -m pytest src/year<YEAR>/test_day<DAY>.py
  ```

### Step 4: Submission
- **Method 1 (Preferred)**: Use the `submit_answer` function in `src.utils`.
- **Method 2 (CLI)**:
  ```bash
  python main.py --year <YEAR> --day <DAY> --part <PART> --submit
  ```

## 3. Important Commands Reference

### Fetch Problem Description
```bash
python fetch_puzzle.py --year <YEAR> --day <DAY> --output day<DAY>_desc.html
```

### Verify Environment
```bash
# Check if pytest is available
python -m pytest --version
```

### Run Solution
```bash
python main.py --year <YEAR> --day <DAY>
```

### Submit
```bash
# Submit Part 1
python main.py --year <YEAR> --day <DAY> --part 1 --submit
```

