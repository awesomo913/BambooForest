# From: levels.py:538
# The Arid Rift -- wind and scorpion projectiles.

def _build_level_6() -> LevelDef:
    """The Arid Rift -- wind and scorpion projectiles."""
    plats = [
        PlatformDef(400, 420, 220), PlatformDef(950, 380, 180),
        PlatformDef(1500, 410, 240), PlatformDef(2050, 360, 200),
        PlatformDef(2600, 400, 220), PlatformDef(3150, 370, 200),
        PlatformDef(3700, 400, 240), PlatformDef(4250, 380, 200),
        PlatformDef(4800, 410, 240), PlatformDef(5350, 390, 220),
        PlatformDef(5900, 400, 260),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[5], platforms=plats, biome="desert",
        enemies=[
            EnemyDef(1000, FLOOR_Y - 50, "dust_devil", 300),
            EnemyDef(3200, FLOOR_Y - 50, "dust_devil", 280),
            EnemyDef(550, 410, "cactus_scorpion", 120),
            EnemyDef(2100, 350, "cactus_scorpion", 100),
            EnemyDef(4300, 370, "cactus_scorpion", 120),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[5], FLOOR_Y, 18),
        heal_positions=[(1520, 410), (3730, 400), (5370, 390)],
        goal_x=6200, checkpoint_positions=[2200, 4200],
        wind_zones=[
            (800, 200, 200, 300, 1.0),
            (2300, 200, 200, 300, -1.0),
            (3900, 200, 200, 300, 1.0),
            (5100, 200, 200, 300, -1.0),
        ],
        updraft_positions=[(1300, FLOOR_Y), (2900, FLOOR_Y), (4600, FLOOR_Y)],
        npc_defs=[(5500, FLOOR_Y, "Silas",
                   ["Watch the wind patterns...",
                    "Use updrafts to reach high ground."],
                   (180, 160, 80))],
    )
