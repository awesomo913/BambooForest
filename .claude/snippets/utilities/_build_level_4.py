# From: levels.py:473
# The Caldera -- volcanic geysers and toxic slimes.

def _build_level_4() -> LevelDef:
    """The Caldera -- volcanic geysers and toxic slimes."""
    plats = [
        PlatformDef(400, 410, 220), PlatformDef(1000, 360, 200),
        PlatformDef(1600, 400, 240), PlatformDef(2200, 340, 200),
        PlatformDef(2800, 390, 220), PlatformDef(3400, 360, 200),
        PlatformDef(4000, 400, 240), PlatformDef(4600, 380, 260),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[3], platforms=plats, biome="volcanic",
        enemies=[
            EnemyDef(440, 400, "sulfur_slime", 180),
            EnemyDef(1640, 390, "sulfur_slime", 200),
            EnemyDef(2840, 380, "sulfur_slime", 160),
            EnemyDef(800, 280, "ash_bat"), EnemyDef(2500, 260, "ash_bat"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[3], FLOOR_Y, 14),
        heal_positions=[(1020, 360), (3420, 360), (4650, 380)],
        goal_x=5200, checkpoint_positions=[2000, 3800],
        weapon_positions=[(2200, FLOOR_Y)],
        geyser_positions=[
            (700, FLOOR_Y), (1350, FLOOR_Y), (1950, FLOOR_Y),
            (2600, FLOOR_Y), (3200, FLOOR_Y),
        ],
        npc_defs=[(4200, FLOOR_Y, "Cinder",
                   ["The geysers erupt every 3 seconds.",
                    "Ride them to reach high platforms!"],
                   (180, 100, 50))],
    )
