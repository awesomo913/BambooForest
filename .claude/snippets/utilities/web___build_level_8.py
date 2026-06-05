# From: web/levels.py:621
# Salt Flats -- ice physics and phantom enemies.

def _build_level_8() -> LevelDef:
    """Salt Flats -- ice physics and phantom enemies."""
    ice = [
        PlatformDef(400, 420, 240), PlatformDef(950, 380, 200),
        PlatformDef(1500, 410, 260), PlatformDef(2100, 360, 220),
        PlatformDef(2700, 400, 240), PlatformDef(3300, 370, 200),
        PlatformDef(3900, 400, 260), PlatformDef(4500, 380, 220),
        PlatformDef(5100, 410, 260), PlatformDef(5700, 390, 240),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[7], platforms=[], biome="salt",
        is_icy=True, ice_defs=ice,
        enemies=[
            EnemyDef(600, FLOOR_Y, "brine_shard"),
            EnemyDef(1800, FLOOR_Y, "brine_shard"),
            EnemyDef(3500, FLOOR_Y, "brine_shard"),
            EnemyDef(1200, 410, "reflection_phantom", 200),
            EnemyDef(2900, 400, "reflection_phantom", 200),
        ],
        bamboo_positions=_scatter_bamboos(ice, LEVEL_WIDTHS[7], FLOOR_Y, 18),
        heal_positions=[(970, 380), (3320, 370), (5120, 410)],
        goal_x=6700, checkpoint_positions=[2400, 4500, 6000],
        glide_positions=[(2000, FLOOR_Y), (4800, FLOOR_Y)],
        dash_positions=[(3200, FLOOR_Y)],
        npc_defs=[(6200, FLOOR_Y, "Mirage",
                   ["Nothing is what it seems here...",
                    "Watch for phantoms in the reflection."],
                   (200, 140, 80))],
    )
