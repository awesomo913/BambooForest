# From: levels.py:639
# Abyssal Trench -- underwater feel. Uses cave biome dark + crystals.

def _build_level_9() -> LevelDef:
    """Abyssal Trench -- underwater feel. Uses cave biome dark + crystals."""
    plats = [
        PlatformDef(400, 420, 200),
        PlatformDef(900, 380, 220),
        PlatformDef(1400, 350, 180),
        PlatformDef(1900, 400, 200, moving=True, axis="vertical", distance=70),
        PlatformDef(2450, 370, 220),
        PlatformDef(3000, 400, 200),
        PlatformDef(3550, 360, 220, moving=True, axis="horizontal", distance=120),
        PlatformDef(4100, 390, 240),
        PlatformDef(4700, 400, 260),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[8], platforms=plats, biome="cave", is_dark=True,
        enemies=[
            EnemyDef(450, 410, "flying", 200),
            EnemyDef(1450, 340, "flying", 200),
            EnemyDef(2500, 360, "chaser"),
            EnemyDef(3050, 390, "chaser"),
            EnemyDef(3600, 350, "slime", 150),
            EnemyDef(4150, 380, "slime", 150),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[8], FLOOR_Y, 14),
        heal_positions=[(940, 380), (3020, 400), (4730, 400)],
        goal_x=5600, checkpoint_positions=[1700, 3400],
        weapon_positions=[(1200, FLOOR_Y)],
        crystal_positions=[(600, FLOOR_Y), (1700, FLOOR_Y), (2800, FLOOR_Y),
                          (3900, FLOOR_Y), (5000, FLOOR_Y)],
        trenches=[(1720, 1860), (3400, 3520)],
        npc_defs=[(5200, FLOOR_Y, "Luminesce",
                   ["The abyss remembers the light.",
                    "Strike crystals to see your path."],
                   (100, 200, 240))],
    )
