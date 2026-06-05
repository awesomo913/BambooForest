# From: levels.py:676
# Orogeny Peak -- vertical scaling. Many stacked platforms.

def _build_level_10() -> LevelDef:
    """Orogeny Peak -- vertical scaling. Many stacked platforms."""
    plats = [
        PlatformDef(400, 430, 220),
        PlatformDef(750, 370, 180),
        PlatformDef(1100, 310, 160),
        PlatformDef(1450, 380, 200, moving=True, axis="horizontal", distance=120),
        PlatformDef(1850, 330, 160),
        PlatformDef(2200, 400, 200),
        PlatformDef(2600, 350, 180, moving=True, axis="vertical", distance=60),
        PlatformDef(3000, 300, 160),
        PlatformDef(3400, 380, 220),
        PlatformDef(3850, 340, 200),
        PlatformDef(4300, 400, 220),
        PlatformDef(4800, 360, 240),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[9], platforms=plats, biome="basalt",
        enemies=[
            EnemyDef(450, 420, "patrol", 180),
            EnemyDef(1500, 370, "patrol", 180),
            EnemyDef(2250, 390, "patrol", 160),
            EnemyDef(3450, 370, "slime", 200),
            EnemyDef(4350, 390, "slime", 180),
            EnemyDef(1150, 220, "flying", 180),
            EnemyDef(3050, 210, "flying", 200),
            EnemyDef(800, 360, "chaser"),
            EnemyDef(3050, 290, "chaser"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[9], FLOOR_Y, 18),
        heal_positions=[(1470, 380), (3420, 380), (4820, 360)],
        goal_x=5300, checkpoint_positions=[1500, 3200, 4500],
        weapon_positions=[(1000, FLOOR_Y)],
        trenches=[(680, 760), (1840, 1950), (3380, 3490)],
        npc_defs=[(5100, FLOOR_Y, "Kora",
                   ["The mountain tests your endurance.",
                    "Dash past the avalanche zones!"],
                   (255, 255, 255))],
    )
