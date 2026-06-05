# From: levels.py:802
# Crystal Geode -- final level. Dark, crystals, boss + many flying.

def _build_level_13() -> LevelDef:
    """Crystal Geode -- final level. Dark, crystals, boss + many flying."""
    plats = [
        PlatformDef(400, 420, 220),
        PlatformDef(900, 370, 180),
        PlatformDef(1400, 410, 220),
        PlatformDef(1950, 360, 200, moving=True, axis="vertical", distance=50),
        PlatformDef(2500, 400, 220),
        PlatformDef(3050, 370, 200),
        PlatformDef(3550, 400, 240, moving=True, axis="horizontal", distance=100),
        PlatformDef(4100, 380, 220),
        PlatformDef(4600, 400, 260),
        PlatformDef(5100, 420, 900, 20),  # boss arena
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[12], platforms=plats, biome="cave", is_dark=True,
        enemies=[
            EnemyDef(450, 410, "patrol", 180),
            EnemyDef(1450, 400, "slime", 180),
            EnemyDef(2550, 390, "patrol", 180),
            EnemyDef(1000, 360, "chaser"),
            EnemyDef(2000, 350, "chaser"),
            EnemyDef(3600, 390, "chaser"),
            EnemyDef(4150, 370, "chaser"),
            EnemyDef(700, 260, "flying", 200),
            EnemyDef(2200, 250, "flying", 200),
            EnemyDef(3700, 260, "flying", 200),
            EnemyDef(4500, 260, "flying", 200),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[12], FLOOR_Y, 22),
        heal_positions=[(940, 370), (3080, 370), (4130, 380), (4800, FLOOR_Y)],
        goal_x=6700, checkpoint_positions=[1800, 3500, 4900, 5800],
        weapon_positions=[(500, FLOOR_Y), (3200, FLOOR_Y)],
        dash_positions=[(2500, FLOOR_Y)],
        crystal_positions=[(300, FLOOR_Y), (1200, FLOOR_Y), (2200, FLOOR_Y),
                          (3200, FLOOR_Y), (4200, FLOOR_Y), (5400, FLOOR_Y)],
        dark_wall_defs=[(1500, 340, 40, 130), (3700, 340, 40, 130)],
        has_boss=True,
        boss_pos=(5500, FLOOR_Y),
        npc_defs=[(6500, FLOOR_Y, "Core Guardian",
                   ["The corruption ends here.",
                    "Pain-da -- make us proud."],
                   (255, 220, 120))],
    )
