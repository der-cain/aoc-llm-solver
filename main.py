import argparse
import importlib
import sys
import os
import time
from src.utils import get_input, submit_answer

def run_day(year, day, part=None, submit=False):
    print(f"--- Running {year} Day {day} ---")
    try:
        module_name = f"src.year{year}.day{day:02d}"
        module = importlib.import_module(module_name)
    except ImportError:
        print(f"Solution for day {day} not found ({module_name}).")
        return

    try:
        data = get_input(year, day)
    except Exception as e:
        print(f"Error fetching input: {e}")
        return

    if hasattr(module, 'parse'):
        try:
            data = module.parse(data)
        except Exception as e:
            print(f"Error parsing input: {e}")
            return

    if hasattr(module, 'part1'):
        start_time = time.time()
        try:
            result = module.part1(data)
            print(f"Part 1: {result} (in {time.time() - start_time:.4f}s)")
            if submit and result is not None and result != "Not implemented":
                submit_answer(year, day, 1, result)
        except Exception as e:
             print(f"Error executing Part 1: {e}")
             import traceback; traceback.print_exc()
    else:
         print("Part 1 not implemented.")

    if hasattr(module, 'part2'):
        start_time = time.time()
        try:
            result = module.part2(data)
            print(f"Part 2: {result} (in {time.time() - start_time:.4f}s)")
            if submit and result is not None and result != "Not implemented":
                submit_answer(year, day, 2, result)
        except Exception as e:
             print(f"Error executing Part 2: {e}")
             import traceback; traceback.print_exc()
    else:
         print("Part 2 not implemented.")

def main():
    parser = argparse.ArgumentParser(description="Advent of Code 2025 Solver")
    parser.add_argument("--day", type=int, help="Day to solve (1-25)")
    parser.add_argument("--part", type=int, choices=[1, 2], help="Part to solve (1 or 2)")
    parser.add_argument("--year", type=int, default=2025, help="Year to solve (default: 2025)")
    parser.add_argument("--submit", action="store_true", help="Submit answer to AoC")
    
    args = parser.parse_args()
    
    if args.day:
        run_day(args.year, args.day, args.part, args.submit)
    else:
        # Run all implemented days
        print("Running all implemented days...")
        # Simple discovery: check for files in src/year{year}
        year_dir = f"src/year{args.year}"
        if not os.path.exists(year_dir):
             print(f"Directory {year_dir} does not exist.")
             return

        days = []
        for f in os.listdir(year_dir):
            if f.startswith("day") and f.endswith(".py"):
                try:
                    day_num = int(f[3:-3])
                    days.append(day_num)
                except ValueError:
                    pass
        
        for day in sorted(days):
            run_day(args.year, day, args.part, args.submit)
            print("-" * 20)

if __name__ == "__main__":
    main()
