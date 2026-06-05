# From: levels.py:392

def _build_level_1() -> LevelDef:
    plats = [
        PlatformDef(400, 420, 240), PlatformDef(900, 380, 200),
        PlatformDef(1400, 410, 260),
        PlatformDef(1900, 370, 220, moving=True, axis="horizontal", distance=100),
        PlatformDef(2450, 400, 240),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[0], platforms=plats,
        enemies=[EnemyDef(440, 410, "patrol", 180), EnemyDef(1440, 400, "patrol", 200),
                 EnemyDef(2480, 390, "slime", 160)],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[0], FLOOR_Y, 11),
        heal_positions=[(950, 380), (2500, 400)],
        goal_x=2800, checkpoint_positions=[1500],
        weapon_positions=[(700, FLOOR_Y)],
        dash_positions=[(400, FLOOR_Y)],  # L1 intro dash item
    )
