import re
from collections import defaultdict
import heapq

def parse(data):
    # Step C must be finished before step A can begin.
    pattern = re.compile(r'Step (\w) must be finished before step (\w) can begin.')
    deps = defaultdict(set)
    all_steps = set()
    for line in data.splitlines():
        match = pattern.match(line)
        if match:
            u, v = match.groups()
            deps[v].add(u)
            all_steps.add(u)
            all_steps.add(v)
    return deps, sorted(list(all_steps))

def part1(data):
    deps, all_steps = data
    result = []

    completed = set()
    available = []

    # Find steps with no dependencies
    for step in all_steps:
        if not deps[step]:
            heapq.heappush(available, step)

    while available:
        step = heapq.heappop(available)
        result.append(step)
        completed.add(step)

        # Check all steps to see if they are now available
        for s in all_steps:
            if s not in completed and s not in available:
                if deps[s].issubset(completed):
                    heapq.heappush(available, s)

    return "".join(result)

def part2(data):
    deps, all_steps = data

    # Configuration
    num_workers = 5
    base_duration = 60

    workers = [(0, None) for _ in range(num_workers)] # (finish_time, task)

    completed = set()
    available = []
    in_progress = set()

    # Initialize available steps
    for step in all_steps:
        if not deps[step]:
            heapq.heappush(available, step)

    current_time = 0

    while len(completed) < len(all_steps):
        # Check for completed tasks
        workers.sort() # Process earliest finishing workers first

        # We need to advance time to the next event (task completion or just start)
        # But since we have multiple workers, we can just simulate second by second or jump to next event.
        # Jumping to next event is more efficient.

        # Check if any worker finishes at current_time (or before, but we monotonic increase)
        # Actually, let's just simulate loop until all done.

        # Free up workers who are done
        free_workers_indices = []
        for i, (finish_time, task) in enumerate(workers):
            if task is not None and finish_time <= current_time:
                completed.add(task)
                workers[i] = (0, None)
                in_progress.remove(task)

                # Check for new available steps based on this completion
                for s in all_steps:
                    if s not in completed and s not in available and s not in in_progress:
                        if deps[s].issubset(completed):
                            heapq.heappush(available, s)

        # Assign new tasks to free workers
        for i in range(num_workers):
            if workers[i][1] is None:
                if available:
                    step = heapq.heappop(available)
                    duration = base_duration + (ord(step) - ord('A') + 1)
                    workers[i] = (current_time + duration, step)
                    in_progress.add(step)

        # Determine next time jump
        next_event_time = float('inf')
        active = False
        for finish_time, task in workers:
            if task is not None:
                next_event_time = min(next_event_time, finish_time)
                active = True

        if not active:
            if len(completed) == len(all_steps):
                break
            # Deadlock or logic error? Or maybe just waiting for nothing?
            # Should not happen if graph is valid.
            pass
        else:
            current_time = max(current_time, next_event_time)

    return current_time
