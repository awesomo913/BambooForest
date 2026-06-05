# From: levels.py:848
# Fungal Hollows -- bouncy mushroom springs + spore puffers.

def _build_level_14() -> LevelDef:
    """Fungal Hollows -- bouncy mushroom springs + spore puffers."""
    plats = [
        PlatformDef(400, 420, 220),
        PlatformDef(900, 380, 180),
        PlatformDef(1450, 410, 220),
        PlatformDef(2000, 370, 200, moving=True, axis="horizontal", distance=90),
        PlatformDef(2550, 400, 200),
        # High platforms reachable ONLY via mushroom bounce:
        PlatformDef(3100, 280, 160),
        PlatformDef(3600, 290, 160),
        PlatformDef(4100, 400, 220),
        PlatformDef(4600, 360, 200, moving=True, axis="vertical", distance=50),
        PlatformDef(5200, 400, 260),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[13], platforms=plats, biome="mushroom",
        enemies=[
            EnemyDef(440, 410, "patrol", 180),
            EnemyDef(1490, 400, "slime", 180),
            EnemyDef(800, 360, "spore_puffer"),
            EnemyDef(2600, 390, "spore_puffer"),
            EnemyDef(4150, 390, "spore_puffer"),
            EnemyDef(4700, 360, "chaser"),
            EnemyDef(1500, 260, "flying", 180),
            EnemyDef(3300, 260, "flying", 180),
            EnemyDef(2600, 150, "homing_specter"),
            EnemyDef(4500, 150, "homing_specter"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[13], FLOOR_Y, 16),
        heal_positions=[(950, 380), (3120, 280), (5230, 400)],
        goal_x=5800, checkpoint_positions=[2000, 4200],
        weapon_positions=[(1200, FLOOR_Y)],
        mushroom_positions=[
            (2800, FLOOR_Y), (3350, FLOOR_Y), (3850, FLOOR_Y),
            (4400, FLOOR_Y), (5000, FLOOR_Y),
        ],
        crumbling_defs=[
            PlatformDef(1750, 380, 120),
            PlatformDef(3350, 280, 100),  # crumbles after bounce
            PlatformDef(4900, 370, 120),
        ],
        crystal_positions=[(700, FLOOR_Y), (3900, FLOOR_Y)],
        trenches=[(1250, 1400), (3700, 3850)],
        glide_positions=[(5200, FLOOR_Y)],
        npc_defs=[(5400, FLOOR_Y, "Myco",
                   ["Land on the mushroom caps to bounce super high!",
                    "Watch out -- specters track you in the air!"],
                   (180, 120, 200))],
    )
