# From: levels.py:504
# Basalt Columns -- crumbling platforms and armored crabs.

def _build_level_5() -> LevelDef:
    """Basalt Columns -- crumbling platforms and armored crabs."""
    plats = [
        PlatformDef(400, 420, 200), PlatformDef(950, 380, 180),
        PlatformDef(1500, 410, 220), PlatformDef(2100, 370, 200),
        PlatformDef(2650, 400, 220), PlatformDef(3200, 380, 200),
        PlatformDef(3750, 410, 240),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[4], platforms=plats, biome="basalt",
        enemies=[
            EnemyDef(440, 410, "kelp_crab", 160),
            EnemyDef(1540, 400, "kelp_crab", 180),
            EnemyDef(2690, 390, "kelp_crab", 140),
            EnemyDef(1200, 380, "basalt_golem"),
            EnemyDef(2400, 370, "basalt_golem"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[4], FLOOR_Y, 14),
        heal_positions=[(980, 380), (2680, 400)],
        goal_x=4700, checkpoint_positions=[1800, 3300],
        weapon_positions=[(2000, FLOOR_Y)],
        dash_positions=[(500, FLOOR_Y)],
        crumbling_defs=[
            PlatformDef(700, 400, 120), PlatformDef(1250, 350, 100),
            PlatformDef(1850, 380, 120), PlatformDef(2400, 340, 100),
            PlatformDef(3000, 370, 120),
        ],
        npc_defs=[(3500, FLOOR_Y, "Finn",
                   ["These columns are ancient basalt.",
                    "Some crumble... be quick on your feet!"],
                   (40, 40, 40))],
    )
