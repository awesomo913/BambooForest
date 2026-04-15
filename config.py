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
PLAYER_MAX_HP: int = 100
PLAYER_INVINCIBLE_SEC: float = 0.5
PLAYER_DAMAGE: int = 25
HEAL_AMOUNT: int = 25
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
BOSS_HP: int = 5
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
ICE_FRICTION: float = 0.97     # per-frame velocity multiplier (slide feel)
ICE_ACCEL: float = 1500.0      # px/s^2 -- meaningful acceleration on ice
BRINE_GROW_RATE: float = 0.5
BRINE_DMG_RADIUS: float = 40.0
PHANTOM_SPEED: float = 100.0

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

# --- Levels ---
LEVEL_COUNT: int = 13
LEVEL_WIDTHS: list[int] = [
    3000, 4500, 6000, 5500, 5000, 6500, 5500, 7000,
    6000, 5500, 6000, 6500, 7000,
]
LEVEL_NAMES: list[str] = [
    "Bamboo Grove", "Mountain Pass", "Mutant Lair",
    "The Caldera", "Basalt Columns", "The Arid Rift",
    "Karst Caves", "Salt Flats",
    "Abyssal Trench", "Orogeny Peak", "Hypersaline Rift",
    "Tabletop Canopy", "Crystal Geode",
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

# --- Paths ---
if getattr(sys, "frozen", False):
    BASE_DIR: str = sys._MEIPASS  # type: ignore[attr-defined]
else:
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
_EXE_DIR: str = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else BASE_DIR
SAVE_FILE: str = os.path.join(_EXE_DIR, "highscores.json")
MUTANT_PNG: str = os.path.join(BASE_DIR, "mutant.png")
