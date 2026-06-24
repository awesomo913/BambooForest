"""All game constants, colors, and tuning parameters."""

import os
import sys

# --- Display ---
SCREEN_WIDTH: int = 960
SCREEN_HEIGHT: int = 540
FPS: int = 60
TITLE: str = "Bamboo Forest"

# --- Physics (per-second, multiplied by dt) ---
GRAVITY: float = 1800.0
PLAYER_SPEED: float = 360.0
PLAYER_JUMP: float = -660.0
TERMINAL_VELOCITY: float = 720.0
PLAYER_SIZE: tuple[int, int] = (36, 44)

# --- Player Stats ---
PLAYER_MAX_HP: int = 120     # 5 hits to die (was 4) -- more forgiving
PLAYER_INVINCIBLE_SEC: float = 0.8  # longer i-frames (was 0.5)
PLAYER_DAMAGE: int = 20      # each hit costs 20 (was 25)
HEAL_AMOUNT: int = 30
DOUBLE_JUMP_LEVEL: int = 0
STARTING_LIVES: int = 3

# --- Enemy (shared) ---
ENEMY_PATROL_SPEED: float = 120.0
ENEMY_CHASE_SPEED: float = 180.0
ENEMY_CHASE_RANGE: float = 500.0
ENEMY_CHASE_Y_RANGE: float = 250.0
ENEMY_STOMP_BOUNCE: float = -400.0
FLYING_ENEMY_AMP: float = 60.0
FLYING_ENEMY_FREQ: float = 2.0
SLIME_BOUNCE_SPEED: float = 150.0
SLIME_HOP_POWER: float = -350.0
SAFE_ZONE_WIDTH: int = 400

# --- Boss ---
BOSS_HP: int = 7
BOSS_SIZE: tuple[int, int] = (90, 90)
BOSS_CHARGE_SPEED: float = 300.0
BOSS_STUN_SEC: float = 1.5
BOSS_IDLE_SEC: float = 1.5

# --- Combo ---
COMBO_WINDOW: float = 2.0
COMBO_MULTIPLIERS: list[int] = [1, 2, 3, 4]
BAMBOO_SCORE: int = 100
STOMP_SCORE: int = 200
BOSS_KILL_SCORE: int = 1000

# --- Moving Platforms ---
MOVING_PLAT_SPEED: float = 80.0

# --- Particles ---
LEAF_COUNT: int = 25
SPARKLE_LIFE: float = 0.4
DUST_LIFE: float = 0.3
SHAKE_INTENSITY: int = 8
SHAKE_DURATION: float = 0.2

# --- Level 4: Caldera (Volcanic) ---
GEYSER_INTERVAL: float = 3.0
GEYSER_DURATION: float = 1.0
GEYSER_LAUNCH: float = -900.0
SULFUR_SPEED: float = 60.0
SULFUR_TRAIL_DMG: int = 10
SULFUR_TRAIL_LIFE: float = 3.0
ASH_BAT_SWOOP: float = 200.0
ASH_BAT_RANGE: float = 300.0

# --- Level 5: Basalt Columns ---
CRUMBLE_DELAY: float = 1.0
CRUMBLE_RESPAWN: float = 4.0
KELP_CRAB_SPEED: float = 80.0
GOLEM_STRIKE_RANGE: float = 80.0
GOLEM_STRIKE_SPEED: float = 250.0
GOLEM_COOLDOWN: float = 2.0

# --- Level 6: Arid Rift (Desert) ---
WIND_PUSH: float = 200.0
THERMAL_FORCE: float = -500.0
DUST_DEVIL_SPEED: float = 150.0
SCORPION_FIRE_RATE: float = 2.0
SCORPION_PROJ_SPEED: float = 250.0

# --- Level 7: Karst Caves (Darkness) ---
DARK_RADIUS: int = 120
CRYSTAL_RADIUS: int = 250
CRYSTAL_LIGHT_TIME: float = 8.0
SPIDER_DROP_RANGE: float = 100.0
SPIDER_DROP_SPEED: float = 400.0
GLOWWORM_SNAP_RANGE: float = 60.0

# --- Level 8: Salt Flats (Ice) ---
ICE_FRICTION: float = 0.90     # final tuned 0.90 (per-frame mult); ~1.5-2s coast feel on ice with snap-to-zero logic
ICE_ACCEL: float = 1500.0      # px/s^2 -- meaningful acceleration on ice
BRINE_GROW_RATE: float = 0.5
BRINE_DMG_RADIUS: float = 40.0
PHANTOM_SPEED: float = 100.0

# --- Power-up Durations ---
GLIDE_DURATION_SEC: float = 10.0
DASH_DURATION_SEC: float = 30.0

# --- Controls (jump feel) ---
JUMP_BUFFER_TIME: float = 0.10   # seconds to queue a jump before landing (buffer + coyote for forgiveness)
JUMP_CUT_MULTIPLIER: float = 0.55  # velocity multiplier when releasing jump early (variable height; tap=short hop)
COYOTE_TIME: float = 0.12        # seconds of post-leave-ground forgiveness (crisp 0.12s ~7 frames; forgiving ledges w/o floaty/easy)
AIR_ACCEL: float = 1580.0        # air control accel px/s2 (tuned for crisp turns + steer without losing momentum feel)
HITSTOP_LAND_SEC: float = 0.032  # tiny juice: very brief x-damp on land for planty "snap" (forgiving stop w/o stick)

# --- Level 14: Fungal Hollows ---
MUSHROOM_BOUNCE: float = -1100.0
MUSHROOM_COMPRESS_SEC: float = 0.15
SPORE_INTERVAL: float = 3.0
SPORE_LIFETIME: float = 4.0
SPORE_DRIFT: float = 40.0
SPORE_DAMAGE: int = 15

# --- Level 15: The Crucible (Rising Lava) ---
LAVA_RISE_SPEED: float = 25.0
LAVA_PAUSE_SEC: float = 3.0
LAVA_START_Y: int = 600
LEAPER_JUMP: float = -700.0
LEAPER_INTERVAL: float = 4.0

# --- Level 16: Tidal Locks (Timed Gates) ---
GATE_CYCLE_SEC: float = 3.0
GATE_TELEGRAPH_SEC: float = 0.5
TIDAL_CRAB_SPEED: float = 90.0

# --- Level 17: Phantom Corridor (Portals) ---
PORTAL_COOLDOWN_SEC: float = 2.0
WRAITH_SPEED: float = 110.0

# --- Level 18: The Gravity Engine ---
GRAVITY_LOW_MULT: float = 0.3
GRAVITY_HIGH_MULT: float = 2.0
GRAVITY_REVERSE_MULT: float = -1.0
DRONE_RANGE: float = 200.0
DRONE_PULL: float = 150.0

# --- NPC ---
NPC_RANGE: float = 60.0

# --- Colors ---
COL_SKY = (135, 206, 235)
COL_PANDA_BLACK = (30, 30, 30)
COL_PANDA_WHITE = (240, 240, 235)
COL_BAMBOO = (76, 153, 0)
COL_BAMBOO_JOINT = (50, 120, 0)
COL_PLAT_GRASS = (34, 139, 34)
COL_PLAT_DIRT = (101, 67, 33)
COL_HEAL_PINK = (255, 105, 180)
COL_HEAL_RED = (220, 20, 60)
COL_GOLD = (255, 215, 0)
COL_HUD_BG = (20, 20, 20)
COL_HP_RED = (180, 30, 30)
COL_HP_GREEN = (30, 200, 30)
COL_MOUNTAIN_FAR = (100, 130, 160)
COL_MOUNTAIN_MID = (80, 110, 80)
COL_TREE_TRUNK = (90, 60, 30)
COL_TREE_CANOPY = (40, 120, 40)
COL_FOLIAGE = (30, 100, 30)
COL_MENU_BG = (20, 40, 20)
COL_WHITE = (255, 255, 255)
COL_RED = (255, 0, 0)
COL_BLACK = (0, 0, 0)
COL_LAVA = (180, 80, 40)
COL_BASALT = (60, 60, 70)
COL_SANDSTONE = (194, 160, 100)
COL_LIMESTONE = (180, 175, 160)
COL_SALT = (200, 220, 240)
COL_TOXIC = (120, 200, 40)
COL_ICE = (180, 220, 255)
COL_CRYSTAL = (100, 200, 255)
COL_MUSHROOM = (180, 60, 160)
COL_TIDAL = (60, 100, 140)
COL_GRAVITY = (80, 50, 120)

# --- Levels ---
LEVEL_COUNT: int = 18
LEVEL_WIDTHS: list[int] = [
    3000, 4500, 6000, 5500, 5000, 6500, 5500, 7000,
    6000, 5500, 6000, 6500, 7000,
    6000, 6500, 6000, 5500, 7500,
]
LEVEL_NAMES: list[str] = [
    "Bamboo Grove", "Corrupted Thicket", "Mutant Lair",
    "The Caldera", "Basalt Columns", "The Arid Rift",
    "Karst Caves", "Salt Flats",
    "Abyssal Trench", "Orogeny Peak", "Hypersaline Rift",
    "Tabletop Canopy", "Crystal Geode",
    "Fungal Hollows", "The Crucible", "Tidal Locks",
    "Phantom Corridor", "The Gravity Engine",
]
FLOOR_Y: int = 490
TRENCH_DEATH_Y: int = 560  # fall below this = death

# --- Game States ---
ST_MENU = "MENU"
ST_PLAYING = "PLAYING"
ST_PAUSED = "PAUSED"
ST_GAME_OVER = "GAME_OVER"
ST_VICTORY = "VICTORY"
ST_LEVEL_TRANS = "LEVEL_TRANS"
ST_GROVE = "GROVE"
ST_OVERGROWN = "OVERGROWN"  # basic post-game state entry (victory offers if unlocked)

# --- Paths ---
if getattr(sys, "frozen", False):
    BASE_DIR: str = sys._MEIPASS  # type: ignore[attr-defined]
else:
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
_EXE_DIR: str = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else BASE_DIR
SAVE_FILE: str = os.path.join(_EXE_DIR, "highscores.json")
MUTANT_PNG: str = os.path.join(BASE_DIR, "mutant.png")

# --- Accessibility (defaults; actual values live in profile via save.py) ---
# Basic options per spec: particle density, shake intensity, text scale, reduced motion (skips sparkles).
# Other keys retained for forward compat with existing profiles/UI.
DEFAULT_ACCESSIBILITY: dict = {
    "volume": 0.8,               # 0.0 mute ... 1.0 full
    "particle_density": 1.0,     # 0.5 / 1.0 / 1.5
    "shake_intensity": 1.0,      # 0.5 / 1.0 / 1.5
    "text_scale": 1.0,           # 0.75 small ... 1.5 large
    "reduced_motion": False,     # skips some sparkles for accessibility
    "color_filter": 0,           # 0=off, 1=grayscale, 2=warm, 3=high contrast, 4=colorblind
    "game_speed": 1.0,           # 0.5 slow ... 1.5 fast
    "difficulty": "normal",      # "normal" | "easy"
    "fullscreen": False,
}
ACCESSIBILITY_RANGES: dict = {
    "volume": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    "particle_density": [0.5, 1.0, 1.5],
    "shake_intensity": [0.5, 1.0, 1.5],
    "text_scale": [0.75, 1.0, 1.25, 1.5],
    "reduced_motion": [False, True],
    "color_filter": [0, 1, 2, 3, 4],
    "game_speed": [0.5, 0.75, 1.0, 1.25, 1.5],
    "difficulty": ["normal", "easy"],
    "fullscreen": [False, True],
}
ACCESSIBILITY_LABELS: dict = {
    "volume": lambda v: f"{int(v*100)}%",
    "particle_density": lambda v: f"{v:.1f}x",
    "shake_intensity": lambda v: f"{v:.1f}x",
    "text_scale": lambda v: f"{v:.2f}x",
    "reduced_motion": lambda v: "On" if v else "Off",
    "color_filter": lambda v: ["Off", "Grayscale", "Warm tint", "High contrast", "Colorblind"][int(v)] if 0 <= int(v) < 5 else "Off",
    "game_speed": lambda v: f"{v:.2f}x",
    "difficulty": lambda v: v.capitalize(),
    "fullscreen": lambda v: "On" if v else "Off",
}

# --- Speedrun / Ghost (lightweight) ---
GHOST_SAMPLE_INTERVAL: float = 0.2  # record (t, x, y, facing) every 0.2s when speedrun_mode
GHOST_ALPHA: int = 105  # semi-transparent for ghost panda draw
PROJECTILE_WORLD_WIDTH: int = 10000  # for bounds in projectiles without level ref
SHURIKEN_SPEED: float = 600.0
ICE_PROJECTILE_SPEED: float = 800.0

# --- Grove Grafting: combine bench (2-3 essences from BIOME keys -> recipes) ---
# Essences are biome-tagged (earned per-biome on bamboo/run end).
# Recipes require exact set (order independent) of 2 or 3 distinct biome essences.
BIOME_ESSENCE: dict[str, str] = {
    "forest": "verdant",
    "corrupted": "corrupt",
    "lair": "mutant",
    "volcanic": "magma",
    "basalt": "stone",
    "desert": "wind",
    "cave": "crystal",
    "salt": "brine",
    "mushroom": "spore",
    "forge": "forge",
    "tidal": "tide",
    "void": "shadow",
    "gravity": "grav",
}
RECIPES: list[dict] = [
    {"essences": ["volcanic", "basalt"], "graft": "lava_resist", "name": "Lava Walk", "desc": "Rising lava deals heavy damage instead of instant death"},
    {"essences": ["forest", "desert"], "graft": "glide_efficiency", "name": "Wind Rider", "desc": "Glide efficiency: much slower fall while gliding"},
    {"essences": ["lair", "forest"], "graft": "dash_mastery", "name": "Dash Mastery", "desc": "Dash mastery: shorter cooldown between dashes"},
    {"essences": ["salt", "cave", "forest"], "graft": "ice_armor", "name": "Ice Armor", "desc": "Ice armor: resist hazards and gain minor defense"},
    {"essences": ["mushroom", "forge"], "graft": "hp_boost", "name": "Vital Sap", "desc": "Vital sap: +1 starting HP"},
    {"essences": ["basalt", "desert"], "graft": "bamboo_yield", "name": "Bamboo Yield", "desc": "Bamboo yield: +10 score per bamboo"},
    {"essences": ["forest", "corrupted"], "graft": "combo_bonus", "name": "Combo Boost", "desc": "Combo bonus: stronger scaling on combos"},
    {"essences": ["volcanic", "gravity"], "graft": "weak_glide", "name": "Feather Fall", "desc": "Weak glide: mild permanent slow-fall"},
]
