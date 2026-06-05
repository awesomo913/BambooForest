# From: levels.py:900
# The Crucible -- rising lava, constant upward pressure.

def _build_level_15() -> LevelDef:
    """The Crucible -- rising lava, constant upward pressure."""
    plats = [
        # Ascending platforms, left-to-right climb
        PlatformDef(400, 430, 240),
        PlatformDef(950, 380, 200),
        PlatformDef(1500, 410, 200),
        PlatformDef(2050, 360, 180, moving=True, axis="vertical", distance=50),
        PlatformDef(2550, 330, 160),
        PlatformDef(3050, 370, 180),
        PlatformDef(3550, 300, 160),
        PlatformDef(4050, 340, 180, moving=True, axis="vertical", distance=60),
        PlatformDef(4550, 290, 160),
        PlatformDef(5050, 330, 180),
        PlatformDef(5550, 280, 160),
        PlatformDef(6050, 320, 200),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[14], platforms=plats, biome="forge",
        enemies=[
            # Industrial forge denizens -- NOT volcanic reuse
            EnemyDef(800, 430, "forge_hammer"),
            EnemyDef(1700, 410, "forge_hammer"),
            EnemyDef(2700, 330, "forge_hammer"),
            EnemyDef(3700, 300, "forge_hammer"),
            EnemyDef(4700, 290, "forge_hammer"),
            EnemyDef(5500, 280, "forge_hammer"),
            # Aerial trackers
            EnemyDef(2200, 200, "homing_specter"),
            EnemyDef(4200, 200, "homing_specter"),
            EnemyDef(5600, 200, "homing_specter"),
            # Ground patrol
            EnemyDef(500, 420, "patrol", 180),
            EnemyDef(3100, 360, "magma_leaper"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[14], FLOOR_Y, 16),
        heal_positions=[(1520, 410), (3570, 300), (5570, 280)],
        goal_x=6400, checkpoint_positions=[2200, 4300],
        rising_lava=True,
        lava_pause_ys=[460, 410, 360, 310],
        geyser_positions=[(800, FLOOR_Y), (2800, 400), (4300, 360)],
        dash_positions=[(400, 420)],
        npc_defs=[(6200, 310, "Vulcan",
                   ["The forge hammers crush what lava doesn't burn.",
                    "Dodge the slamming anvils and keep climbing!"],
                   (220, 100, 40))],
    )
