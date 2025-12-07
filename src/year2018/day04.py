import re
from collections import defaultdict, Counter
from datetime import datetime

def parse(data):
    lines = data.splitlines()
    lines.sort()
    return lines

def process_data(lines):
    guards = defaultdict(lambda: defaultdict(int)) # guard_id -> minute -> count
    current_guard = None
    asleep_start = None

    # [1518-11-01 00:00] Guard #10 begins shift
    # [1518-11-01 00:05] falls asleep
    # [1518-11-01 00:25] wakes up

    pattern_guard = re.compile(r'\[(.*)\] Guard #(\d+) begins shift')
    pattern_asleep = re.compile(r'\[(.*)\] falls asleep')
    pattern_wake = re.compile(r'\[(.*)\] wakes up')

    for line in lines:
        match_guard = pattern_guard.match(line)
        if match_guard:
            current_guard = int(match_guard.group(2))
            continue

        match_asleep = pattern_asleep.match(line)
        if match_asleep:
            timestamp = datetime.strptime(match_asleep.group(1), "%Y-%m-%d %H:%M")
            asleep_start = timestamp.minute
            continue

        match_wake = pattern_wake.match(line)
        if match_wake:
            timestamp = datetime.strptime(match_wake.group(1), "%Y-%m-%d %H:%M")
            wake_minute = timestamp.minute
            for m in range(asleep_start, wake_minute):
                guards[current_guard][m] += 1
            continue

    return guards

def part1(data):
    guards = process_data(data)

    # Strategy 1: Find the guard that has the most minutes asleep.
    max_sleep_guard = None
    max_sleep_minutes = -1

    for guard, minutes in guards.items():
        total_sleep = sum(minutes.values())
        if total_sleep > max_sleep_minutes:
            max_sleep_minutes = total_sleep
            max_sleep_guard = guard

    if max_sleep_guard is None:
        return 0

    # What minute does that guard spend asleep the most?
    most_asleep_minute = max(guards[max_sleep_guard], key=guards[max_sleep_guard].get)

    return max_sleep_guard * most_asleep_minute

def part2(data):
    guards = process_data(data)

    # Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?
    max_freq_guard = None
    max_freq_minute = -1
    max_freq_count = -1

    for guard, minutes in guards.items():
        if not minutes:
            continue
        minute = max(minutes, key=minutes.get)
        count = minutes[minute]

        if count > max_freq_count:
            max_freq_count = count
            max_freq_minute = minute
            max_freq_guard = guard

    return max_freq_guard * max_freq_minute
