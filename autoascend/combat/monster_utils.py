# heuristic monster types lists
ONLY_RANGED_SLOW_MONSTERS = ['floating eye', 'blue jelly', 'brown mold', 'gas spore', 'acid blob']
EXPLODING_MONSTERS = ['yellow light', 'gas spore', 'flaming sphere', 'freezing sphere', 'shocking sphere']
INSECTS = ['giant ant', 'killer bee', 'soldier ant', 'fire ant', 'giant beetle', 'queen bee']
WEAK_MONSTERS = ['lichen', 'newt', 'shrieker', 'grid bug']
WEIRD_MONSTERS = ['leprechaun', 'nymph']


def is_monster_faster(agent, monster):
    _, y, x, mon, _ = monster
    # hypothesis: use each monster's movement speed so combat heuristics handle fast threats beyond a name list.
    return getattr(mon, 'mmove', 12) > 12


def melee_danger_threshold(agent, monster):
    _, _, _, mon, _ = monster
    baseline = 16 if is_dangerous_monster(monster) else 8
    level_gap = max(0, getattr(mon, 'mlevel', 0) - agent.blstats.experience_level)
    speed_margin = max(0, getattr(mon, 'mmove', 12) - 12)
    # hypothesis: scale low-health caution to how much a monster outlevels the hero.
    return min(24, baseline + round(3 * level_gap + 0.5 * speed_margin))


def imminent_death_on_melee(agent, monster):
    return agent.blstats.hitpoints <= melee_danger_threshold(agent, monster)


def is_dangerous_monster(monster):
    _, y, x, mon, _ = monster
    is_pet = 'dog' in mon.mname or 'cat' in mon.mname or 'kitten' in mon.mname or 'pony' in mon.mname \
             or 'horse' in mon.mname
    # 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
    # or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
    # or 'mimic' in mon.mname
    return is_pet or mon.mname in INSECTS


def consider_melee_only_ranged_if_hp_full(agent, monster):
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
