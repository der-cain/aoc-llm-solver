import os
import requests
import sys

def fetch_description():
    url = "https://adventofcode.com/2025/day/9"
    session = os.environ.get("AOC_SESSION")
    if not session:
        print("AOC_SESSION not found")
        sys.exit(1)

    cookies = {"session": session}
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_description()
