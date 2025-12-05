import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_session_cookie():
    return os.getenv("AOC_SESSION")

def get_input(year, day):
    """
    Fetches input for a given year and day.
    Tries to read from inputs/{year}/day{day:02d}.txt first.
    If not found, fetches from the web and saves it.
    """
    input_path = f"inputs/{year}/day{day:02d}.txt"
    
    if os.path.exists(input_path):
        with open(input_path, 'r') as f:
            return f.read()
    
    session = get_session_cookie()
    if not session:
        raise ValueError("AOC_SESSION environment variable not set. Cannot fetch input.")
    
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session}
    headers = {"User-Agent": "github.com/der-cain/aoc-llm-solver by marius@example.com"}
    
    response = requests.get(url, cookies=cookies, headers=headers)
    response.raise_for_status()
    
    data = response.text
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    
    with open(input_path, 'w') as f:
        f.write(data)
        
    return data

def submit_answer(year, day, part, answer):
    """
    Submits an answer to AoC.
    """
    session = get_session_cookie()
    if not session:
        print("AOC_SESSION not set, cannot submit.")
        return

    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    cookies = {"session": session}
    headers = {
        "User-Agent": "github.com/der-cain/aoc-llm-solver by marius@example.com",
        "Referer": f"https://adventofcode.com/{year}/day/{day}",
        "Origin": "https://adventofcode.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"level": part, "answer": answer}
    
    response = requests.post(url, cookies=cookies, headers=headers, data=payload)
    response.raise_for_status()
    
    text = response.text
    if "That's the right answer" in text:
        print("Status: CORRECT! Star acquired.")
    elif "That's not the right answer" in text:
        print("Status: WRONG Answer.")
    elif "You gave an answer too recently" in text:
        print("Status: RATE LIMITED. Please wait.")
    elif "You don't seem to be solving the right level" in text:
        print("Status: ALREADY SOLVED or invalid level.")
    else:
        print(f"Status: Unknown response. Preview: {text[:200]}...")
