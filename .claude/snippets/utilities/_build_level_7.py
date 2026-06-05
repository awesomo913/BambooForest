# From: levels.py:574
# Karst Caves -- darkness with crystal lights.

def _build_level_7() -> LevelDef:
    """Karst Caves -- darkness with crystal lights."""
    plats = [
        PlatformDef(400, 420, 220), PlatformDef(900, 380, 180),
        PlatformDef(1400, 410, 240), PlatformDef(1900, 360, 200),
        PlatformDef(2450, 400, 220), PlatformDef(2950, 370, 200),
        PlatformDef(3500, 400, 240), PlatformDef(4050, 380, 200),
        PlatformDef(4600, 410, 260),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[6], platforms=plats,
        biome="cave", is_dark=True,
        enemies=[
            EnemyDef(600, 50, "stalactite_spider"),
            EnemyDef(1200, 60, "stalactite_spider"),
            EnemyDef(2200, 50, "stalactite_spider"),
            EnemyDef(3300, 60, "stalactite_spider"),
            EnemyDef(800, 350, "false_glowworm"),
            EnemyDef(1700, 320, "false_glowworm"),
            EnemyDef(2800, 340, "false_glowworm"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[6], FLOOR_Y, 16),
        heal_positions=[(1420, 410), (2970, 370), (4080, 380)],
        goal_x=5200, checkpoint_positions=[1500, 2800, 4100],
        crystal_positions=[
            (300, FLOOR_Y), (750, FLOOR_Y), (1250, FLOOR_Y),
            (1800, FLOOR_Y), (2500, FLOOR_Y), (3200, FLOOR_Y), (3900, FLOOR_Y),
        ],
        dark_wall_defs=[(1100, 340, 40, 130), (2900, 340, 40, 130)],
        npc_defs=[(4300, FLOOR_Y, "Nyx",
                   ["I can hear the echoes of danger...",
                    "Strike the crystals to see!"],
                   (100, 60, 120))],
    )
