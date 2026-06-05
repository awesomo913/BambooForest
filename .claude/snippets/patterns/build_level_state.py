# From: levels.py:1162

def build_level_state(level_number: int) -> LevelState:
    level_def = _BUILDERS[level_number]()
    _verify_jump_arc(level_def)  # raise ValueError if unreachable platforms
    return LevelState(level_def, level_number)
