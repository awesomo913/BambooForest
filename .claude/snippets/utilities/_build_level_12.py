# From: levels.py:753
# Tabletop Canopy -- dense small platforms (jungle vine feel).

def _build_level_12() -> LevelDef:
    """Tabletop Canopy -- dense small platforms (jungle vine feel)."""
    plats = [
        PlatformDef(350, 420, 140),
        PlatformDef(600, 370, 120),
        PlatformDef(830, 410, 140),
        PlatformDef(1050, 350, 120, moving=True, axis="horizontal", distance=80),
        PlatformDef(1300, 390, 140),
        PlatformDef(1550, 330, 120),
        PlatformDef(1800, 380, 140),
        PlatformDef(2100, 350, 140, moving=True, axis="vertical", distance=50),
        PlatformDef(2400, 400, 160),
        PlatformDef(2750, 350, 140),
        PlatformDef(3100, 390, 160),
        PlatformDef(3500, 360, 140, moving=True, axis="horizontal", distance=90),
        PlatformDef(3900, 400, 180),
        PlatformDef(4300, 370, 160),
        PlatformDef(4700, 400, 200),
        PlatformDef(5200, 380, 240),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[11], platforms=plats, biome="forest",
        enemies=[
            EnemyDef(400, 410, "patrol", 120),
            EnemyDef(1350, 380, "patrol", 120),
            EnemyDef(2450, 390, "patrol", 140),
            EnemyDef(3550, 350, "slime", 120),
            EnemyDef(4350, 360, "slime", 120),
            EnemyDef(880, 300, "flying", 160),
            EnemyDef(2500, 260, "flying", 180),
            EnemyDef(4000, 260, "flying", 180),
            EnemyDef(1900, 370, "chaser"),
            EnemyDef(3150, 380, "chaser"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[11], FLOOR_Y, 22),
        heal_positions=[(1080, 350), (3130, 390), (5230, 380)],
        goal_x=6100, checkpoint_positions=[1800, 3400, 4900],
        weapon_positions=[(500, FLOOR_Y)],
        glide_positions=[(200, FLOOR_Y), (2500, FLOOR_Y)],
        dash_positions=[(1200, FLOOR_Y), (4000, FLOOR_Y)],
        trenches=[(490, 580), (970, 1040), (1460, 1540), (2020, 2090),
                  (2920, 3090), (4180, 4290)],
        npc_defs=[(5900, FLOOR_Y, "Capy",
                   ["Rest your paws, traveler.",
                    "This is the longest leg."],
                   (180, 140, 100))],
    )
