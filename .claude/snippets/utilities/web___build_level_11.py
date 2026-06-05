# From: web/levels.py:734
# Hypersaline Rift -- wide gaps needing dash/glide.

def _build_level_11() -> LevelDef:
    """Hypersaline Rift -- wide gaps needing dash/glide."""
    plats = [
        PlatformDef(400, 410, 200),
        PlatformDef(900, 380, 180),
        PlatformDef(1500, 360, 180),   # gap needs glide/dash
        PlatformDef(2100, 400, 220),
        PlatformDef(2700, 370, 200),
        PlatformDef(3300, 390, 220),
        PlatformDef(3900, 360, 200),
        PlatformDef(4500, 400, 240),
        PlatformDef(5100, 380, 220),
        PlatformDef(5700, 400, 260),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[10], platforms=plats, biome="salt", is_icy=True,
        enemies=[
            EnemyDef(450, 400, "reflection_phantom", 180),
            EnemyDef(2150, 390, "reflection_phantom", 200),
            EnemyDef(3350, 380, "brine_shard"),
            EnemyDef(4550, 390, "brine_shard"),
            EnemyDef(1000, 360, "chaser"),
            EnemyDef(3900, 340, "chaser"),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[10], FLOOR_Y, 16),
        heal_positions=[(950, 380), (3350, 390), (5130, 380)],
        goal_x=5900, checkpoint_positions=[2100, 3900],
        weapon_positions=[(600, FLOOR_Y)],
        glide_positions=[(1600, FLOOR_Y), (3600, FLOOR_Y)],
        dash_positions=[(2800, FLOOR_Y)],
        trenches=[(1200, 1440), (2400, 2600), (4200, 4400)],
        npc_defs=[(5600, FLOOR_Y, "Saltbeard",
                   ["The salt ocean looks calm...",
                    "Phantoms strike from reflection!"],
                   (200, 200, 230))],
    )
