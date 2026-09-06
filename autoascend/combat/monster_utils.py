# heuristic monster types lists
ONLY_RANGED_SLOW_MONSTERS = ['floating eye', 'blue jelly', 'brown mold', 'gas spore', 'acid blob']
EXPLODING_MONSTERS = ['yellow light', 'gas spore', 'flaming sphere', 'freezing sphere', 'shocking sphere']
INSECTS = ['giant ant', 'killer bee', 'soldier ant', 'fire ant', 'giant beetle', 'queen bee']
WEAK_MONSTERS = ['lichen', 'newt', 'shrieker', 'grid bug']
WEIRD_MONSTERS = ['leprechaun', 'nymph']


def is_monster_faster(agent, monster):
    _, y, x, mon, _ = monster
    # TOOD: implement properly
    return 'bat' in mon.mname or 'dog' in mon.mname or 'cat' in mon.mname \
           or 'kitten' in mon.mname or 'pony' in mon.mname or 'horse' in mon.mname \
           or 'bee' in mon.mname or 'fox' in mon.mname


def imminent_death_on_melee(agent, monster):
    # hypothesis: characters with at most 50 maximum HP need one extra point of
    # buffer against a rothe's three-hit turn; tougher characters retain the
    # less conservative cutoff so they do not over-kite a manageable fight.
    if monster[3].mname == 'rothe':
        safety_buffer = 26 if agent.blstats.max_hitpoints <= 50 else 25
        return agent.blstats.hitpoints <= safety_buffer
    if is_dangerous_monster(monster, agent):
        return agent.blstats.hitpoints <= 16
    return agent.blstats.hitpoints <= 8


def is_dangerous_monster(monster, agent=None):
    _, y, x, mon, _ = monster
    is_pet = 'dog' in mon.mname or 'cat' in mon.mname or 'kitten' in mon.mname or 'pony' in mon.mname \
             or 'horse' in mon.mname
    # 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
    # or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
    # or 'mimic' in mon.mname
    # hypothesis: treating summoning, infecting werecreatures as dangerous for
    # frail gnome Healers makes them retreat or engrave before a pack traps them.
    vulnerable_to_werecreatures = agent is not None and \
        agent.character.role == agent.character.HEALER and \
        agent.character.race == agent.character.GNOME
    return is_pet or mon.mname in INSECTS or \
        (vulnerable_to_werecreatures and 'were' in mon.mname)


def consider_melee_only_ranged_if_hp_full(agent, monster):
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
