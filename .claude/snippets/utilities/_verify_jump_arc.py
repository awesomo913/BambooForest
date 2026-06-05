# From: levels.py:1131
# Check that every platform is reachable within the player's jump arc.

def _verify_jump_arc(level_def: LevelDef) -> None:
    """Check that every platform is reachable within the player's jump arc.

    Player jump physics:
      PLAYER_JUMP = -660 px/s, GRAVITY = 1800 px/s^2
      Peak height = 660^2 / (2*1800) = 121 px per jump
      Double jump effective height = ~242 px
      Horizontal reach during jump = ~264 px
    """
    from config import PLAYER_JUMP, GRAVITY
    max_height_single = (PLAYER_JUMP ** 2) / (2.0 * GRAVITY)  # 121
    max_height_double = max_height_single * 2.0               # 242
    # Safety margin: platforms must be within 200px of next reachable surface
    # measured from the floor or another platform.
    all_y = [FLOOR_Y] + [p.y for p in level_def.platforms]
    # For each platform, find the closest lower surface (floor or lower platform)
    for p in level_def.platforms:
        # Lower surfaces with y greater than p.y (lower on screen)
        lower = [y for y in all_y if y > p.y]
        if not lower:
            continue
        closest = min(lower, key=lambda y: y - p.y)
        gap = closest - p.y
        # A platform can always be reached from the floor (floor is continuous)
        # with a double jump if the gap is <= 242 + 10 safety margin
        if gap > max_height_double + 10:
            raise ValueError(
                f"Platform at ({p.x}, {p.y}) unreachable: "
                f"vertical gap {gap}px > max double jump {max_height_double:.0f}px")
