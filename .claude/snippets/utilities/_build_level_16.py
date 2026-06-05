# From: levels.py:949
# Tidal Locks -- timed gates cycle every 3 seconds.

def _build_level_16() -> LevelDef:
    """Tidal Locks -- timed gates cycle every 3 seconds."""
    plats = [
        PlatformDef(400, 420, 220),
        PlatformDef(950, 380, 180),
        PlatformDef(2000, 400, 200),  # after first gate section
        PlatformDef(2500, 370, 180),
        PlatformDef(3700, 400, 200),  # after second gate section
        PlatformDef(4200, 380, 180),
        PlatformDef(4700, 410, 220),
        PlatformDef(5200, 380, 240),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[15], platforms=plats, biome="tidal",
        enemies=[
            EnemyDef(440, 410, "tidal_crab", 150),
            EnemyDef(2040, 390, "tidal_crab", 140),
            EnemyDef(3740, 390, "tidal_crab", 150),
            EnemyDef(4740, 400, "patrol", 160),
            EnemyDef(1100, 260, "flying", 200),
            EnemyDef(3000, 260, "flying", 200),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[15], FLOOR_Y, 14),
        heal_positions=[(970, 380), (4220, 380), (5230, 380)],
        goal_x=5800, checkpoint_positions=[2000, 4000],
        weapon_positions=[(1000, FLOOR_Y)],
        # Alternating A/B gates bridging two big trenches
        # First section: 3 gates bridging a gap 1100-1920
        timed_gate_defs=[
            (1200, 400, 120, 20, "A"),
            (1400, 380, 120, 20, "B"),
            (1600, 400, 120, 20, "A"),
            (1800, 380, 120, 20, "B"),
            # Second section: bridge a gap 2800-3600
            (2900, 400, 120, 20, "B"),
            (3100, 380, 120, 20, "A"),
            (3300, 400, 120, 20, "B"),
            (3500, 380, 120, 20, "A"),
        ],
        crumbling_defs=[
            PlatformDef(1100, 420, 80),
            PlatformDef(2700, 400, 100),
        ],
        trenches=[(1130, 1920), (2800, 3600), (4100, 4190)],
        npc_defs=[(5600, FLOOR_Y, "Chronos",
                   ["The ancient locks run on a cycle.",
                    "Watch the glow -- step when it's bright!"],
                   (100, 160, 200))],
    )
