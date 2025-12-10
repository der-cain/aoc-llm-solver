#!/usr/bin/env python3
import argparse
import requests
import sys
import os
import re
from src.utils import get_session_cookie

def fetch_puzzle_description(year, day, output_file=None):
    session = get_session_cookie()
    if not session:
        print("Error: AOC_SESSION environment variable not set. Please check your .env file.")
        sys.exit(1)

    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {"session": session}
    headers = {
        "User-Agent": "github.com/der-cain/aoc-llm-solver by marius@example.com"
    }
    
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        sys.exit(1)

    content = response.text
    
    # Optional: Extract just the article content to reduce noise?
    # Usually AoC pages have <article class="day-desc"> ... </article>
    # There can be multiple articles (Part 1 and Part 2).
    
    articles = re.findall(r'<article class="day-desc">(.*?)</article>', content, re.DOTALL)
    
    if not articles:
        print("Warning: No day-desc articles found in response. Saving full content.")
        final_content = content
    else:
        # Join all articles (Part 1 + Part 2 if available) with a separator
        final_content = "\n\n--- Part Break ---\n\n".join(articles)
        # Convert simple HTML to Markdown-ish text for better readability if desired,
        # but raw HTML is often fine for LLMs or we can just save it.
        # Let's keep it as HTML chunks for now, as that's what the agent usually handles well or converts.
        # Actually, let's wrap it in basic HTML structure so it's a valid viewable file
        final_content = f"<html><body>{''.join(f'<article class=\"day-desc\">{a}</article>' for a in articles)}</body></html>"

    if output_file:
        with open(output_file, 'w') as f:
            f.write(final_content)
        print(f"Puzzle description saved to {output_file}")
    else:
        print(final_content)

def main():
    parser = argparse.ArgumentParser(description="Fetch Advent of Code puzzle description.")
    parser.add_argument("--year", type=int, required=True, help="Year of the puzzle")
    parser.add_argument("--day", type=int, required=True, help="Day of the puzzle")
    parser.add_argument("--output", "-o", type=str, help="Output file path (optional)")

    args = parser.parse_args()

    fetch_puzzle_description(args.year, args.day, args.output)

if __name__ == "__main__":
    main()
