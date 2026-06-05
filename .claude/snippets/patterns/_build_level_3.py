# From: levels.py:439

def _build_level_3() -> LevelDef:
    plats = [
        PlatformDef(400, 420, 220), PlatformDef(900, 370, 180),
        PlatformDef(1400, 410, 240),
        PlatformDef(1950, 360, 200, moving=True, axis="vertical", distance=50),
        PlatformDef(2500, 400, 220), PlatformDef(3050, 370, 200),
        PlatformDef(3550, 400, 240, moving=True, axis="horizontal", distance=100),
        PlatformDef(4100, 380, 220), PlatformDef(4600, 400, 260),
        PlatformDef(5100, 420, 700, 20),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[2], platforms=plats, biome="lair",
        enemies=[EnemyDef(440, 410, "patrol", 180), EnemyDef(1440, 400, "patrol", 200),
                 EnemyDef(2540, 390, "slime", 180), EnemyDef(3090, 360, "patrol", 160),
                 EnemyDef(4140, 370, "patrol", 160), EnemyDef(950, 360, "chaser"),
                 EnemyDef(2000, 350, "chaser"), EnemyDef(3580, 390, "chaser"),
                 EnemyDef(1200, 260, "flying", 200), EnemyDef(2800, 250, "flying", 200),
                 EnemyDef(4300, 260, "flying", 180), EnemyDef(3300, 390, "slime", 160)],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[2], FLOOR_Y, 20),
        heal_positions=[(1450, 410), (3080, 370), (4900, FLOOR_Y)],
        goal_x=5850, checkpoint_positions=[1800, 3500, 4900],
        weapon_positions=[(2500, FLOOR_Y)],
        dash_positions=[(700, FLOOR_Y), (3500, FLOOR_Y)],
        trenches=[(1330, 1470), (2920, 3050), (4380, 4520)],
        has_boss=True, boss_pos=(5500, FLOOR_Y),
        npc_defs=[(4950, FLOOR_Y, "Elder",
                   ["The mutant waits beyond this gate.",
                    "You alone can end this, Pain-da!"],
                   (180, 140, 90))],
    )
