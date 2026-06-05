# From: levels.py:49

@dataclass
class LevelDef:
    world_width: int
    platforms: list[PlatformDef]
    enemies: list[EnemyDef]
    bamboo_positions: list[tuple[int, int]]
    heal_positions: list[tuple[int, int]]
    goal_x: int
    checkpoint_positions: list[int] = field(default_factory=list)
    has_boss: bool = False
    boss_pos: tuple[int, int] = (0, 0)
    player_start: tuple[int, int] = (100, FLOOR_Y)
    # Biome extensions
    biome: str = "forest"
    geyser_positions: list[tuple[int, int]] = field(default_factory=list)
    crumbling_defs: list[PlatformDef] = field(default_factory=list)
    wind_zones: list[tuple[int, int, int, int, float]] = field(default_factory=list)
    updraft_positions: list[tuple[int, int]] = field(default_factory=list)
    crystal_positions: list[tuple[int, int]] = field(default_factory=list)
    ice_defs: list[PlatformDef] = field(default_factory=list)
    npc_defs: list[tuple[int, int, str, list[str], tuple]] = field(default_factory=list)
    weapon_positions: list[tuple[int, int]] = field(default_factory=list)
    glide_positions: list[tuple[int, int]] = field(default_factory=list)
    dash_positions: list[tuple[int, int]] = field(default_factory=list)
    # List of (start_x, end_x) floor gaps that are lethal pits
    trenches: list[tuple[int, int]] = field(default_factory=list)
    is_dark: bool = False
    is_icy: bool = False
    # Levels 14-18
    mushroom_positions: list[tuple[int, int]] = field(default_factory=list)
    rising_lava: bool = False
    lava_pause_ys: list[int] = field(default_factory=list)
    # (x, y, w, h, group_id "A"|"B")
    timed_gate_defs: list[tuple[int, int, int, int, str]] = field(default_factory=list)
    # (x1, y1, x2, y2, pair_id)
    portal_defs: list[tuple[int, int, int, int, int]] = field(default_factory=list)
    # (x, y, w, h, gravity_type "low"|"high"|"reverse")
    gravity_zone_defs: list[tuple[int, int, int, int, str]] = field(default_factory=list)
    # (x, y, w, h) -- walls that block unless nearby crystal is lit
    dark_wall_defs: list[tuple[int, int, int, int]] = field(default_factory=list)
