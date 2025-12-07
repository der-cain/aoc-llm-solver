import re
import copy

def parse(data):
    groups = []
    current_type = ""

    # Army types
    IMMUNE = "Immune System"
    INFECTION = "Infection"

    lines = data.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith("Immune System:"):
            current_type = IMMUNE
            i += 1
            continue
        elif line.startswith("Infection:"):
            current_type = INFECTION
            i += 1
            continue

        # Parse group
        # 18 units each with 729 hit points (weak to fire; immune to cold, slashing) with an attack that does 8 radiation damage at initiative 10
        # Weakness/Immunity part is optional and in parens

        # Regex is hard because of optional parens.
        # Let's split by " units each with " etc.

        match = re.match(r"(\d+) units each with (\d+) hit points (\(.*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)", line)
        if match:
            units = int(match.group(1))
            hp = int(match.group(2))
            attributes_str = match.group(3)
            damage = int(match.group(4))
            damage_type = match.group(5)
            initiative = int(match.group(6))

            weaknesses = set()
            immunities = set()

            if attributes_str:
                # (weak to fire; immune to cold, slashing)
                # Remove parens and space
                attr_content = attributes_str.strip()[1:-1]
                parts = attr_content.split('; ')
                for part in parts:
                    if part.startswith("weak to "):
                        weaks = part[8:].split(', ')
                        weaknesses.update(weaks)
                    elif part.startswith("immune to "):
                        imms = part[10:].split(', ')
                        immunities.update(imms)

            group = {
                'id': f"{current_type} {len([g for g in groups if g['type'] == current_type]) + 1}",
                'type': current_type,
                'units': units,
                'hp': hp,
                'damage': damage,
                'damage_type': damage_type,
                'initiative': initiative,
                'weaknesses': weaknesses,
                'immunities': immunities
            }
            groups.append(group)
        i += 1

    return groups

def effective_power(group):
    return group['units'] * group['damage']

def calculate_damage(attacker, defender):
    if attacker['damage_type'] in defender['immunities']:
        return 0
    dmg = effective_power(attacker)
    if attacker['damage_type'] in defender['weaknesses']:
        return dmg * 2
    return dmg

def solve_combat(groups, boost=0):
    # Apply boost to Immune System
    groups = copy.deepcopy(groups)
    for g in groups:
        if g['type'] == "Immune System":
            g['damage'] += boost

    while True:
        # Check end condition
        immune_alive = [g for g in groups if g['type'] == "Immune System" and g['units'] > 0]
        infection_alive = [g for g in groups if g['type'] == "Infection" and g['units'] > 0]

        if not immune_alive:
            return "Infection", sum(g['units'] for g in infection_alive)
        if not infection_alive:
            return "Immune System", sum(g['units'] for g in immune_alive)

        # Target Selection
        # Sort by effective power (desc), then initiative (desc)
        # Note: Effective power changes as units die

        # We need to sort groups. But effective power depends on current units.
        # Filter alive groups
        alive_groups = [g for g in groups if g['units'] > 0]
        alive_groups.sort(key=lambda g: (-effective_power(g), -g['initiative']))

        targets = {} # attacker_id -> defender
        chosen_defenders = set()

        for attacker in alive_groups:
            # Select target from enemy army
            enemies = [g for g in alive_groups if g['type'] != attacker['type'] and g['id'] not in chosen_defenders]

            if not enemies:
                continue

            # Calculate damage to each enemy
            # Sort enemies by: damage (desc), effective power (desc), initiative (desc)

            def target_key(defender):
                dmg = calculate_damage(attacker, defender)
                return (dmg, effective_power(defender), defender['initiative'])

            enemies.sort(key=target_key, reverse=True)

            best_target = enemies[0]
            dmg = calculate_damage(attacker, best_target)

            if dmg > 0:
                targets[attacker['id']] = best_target
                chosen_defenders.add(best_target['id'])

        # Attacking Phase
        # Attack in decreasing order of initiative
        alive_groups.sort(key=lambda g: -g['initiative'])

        total_units_killed = 0

        for attacker in alive_groups:
            if attacker['units'] <= 0:
                continue

            if attacker['id'] in targets:
                defender = targets[attacker['id']]

                dmg = calculate_damage(attacker, defender)
                killed = min(defender['units'], dmg // defender['hp'])

                defender['units'] -= killed
                total_units_killed += killed

        if total_units_killed == 0:
            # Stalemate check
            return "Stalemate", 0

def part1(data):
    groups = data
    _, units = solve_combat(groups)
    return units

def part2(data):
    groups = data
    # Binary search might not be monotonic? Usually linear search or small binary search.
    # We want MIN boost.
    # Stalemate is possible (units low but damage low -> 0 kills).

    # Try linear search first or step.
    # Boost range? Could be thousands.
    # Start small.

    boost = 1
    while True:
        winner, units = solve_combat(groups, boost)
        if winner == "Immune System":
            return units
        boost += 1
