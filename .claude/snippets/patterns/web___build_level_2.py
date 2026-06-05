# From: web/levels.py:413

def _build_level_2() -> LevelDef:
    plats = [
        PlatformDef(400, 420, 220), PlatformDef(900, 370, 180),
        PlatformDef(1400, 410, 240),
        PlatformDef(1900, 360, 200, moving=True, axis="horizontal", distance=110),
        PlatformDef(2450, 400, 200),
        PlatformDef(2950, 350, 200, moving=True, axis="vertical", distance=50),
        PlatformDef(3450, 390, 240), PlatformDef(3950, 380, 220),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[1], platforms=plats, biome="corrupted",
        enemies=[EnemyDef(440, 410, "patrol", 180), EnemyDef(1440, 400, "patrol", 200),
                 EnemyDef(2480, 390, "patrol", 160), EnemyDef(3480, 380, "slime", 180),
                 EnemyDef(950, 360, "chaser"), EnemyDef(2990, 340, "chaser"),
                 EnemyDef(1700, 260, "flying", 200), EnemyDef(3200, 270, "slime", 150)],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[1], FLOOR_Y, 16),
        heal_positions=[(1450, 410), (3490, 390)],
        goal_x=4200, checkpoint_positions=[1700, 3200],
        weapon_positions=[(2000, FLOOR_Y)],
        glide_positions=[(1000, FLOOR_Y)],
        dash_positions=[(600, FLOOR_Y)],
        trenches=[(1220, 1390), (2600, 2720)],
        npc_defs=[(3900, FLOOR_Y, "Sage",
                   ["The forest is sick... corruption spreads.",
                    "The lair lies ahead. Be ready, Pain-da."],
                   (120, 160, 100))],
    )
