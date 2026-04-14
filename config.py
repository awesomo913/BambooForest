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
DOUBLE_JUMP_LEVEL: int = 0  # always available

# --- Enemy ---
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
BOSS_HP: int = 10
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
STARTING_LIVES: int = 3

# --- Moving Platforms ---
MOVING_PLAT_SPEED: float = 80.0

# --- Particles ---
LEAF_COUNT: int = 25
SPARKLE_LIFE: float = 0.4
DUST_LIFE: float = 0.3
SHAKE_INTENSITY: int = 8
SHAKE_DURATION: float = 0.2

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

# --- Levels ---
LEVEL_COUNT: int = 3
LEVEL_WIDTHS: list[int] = [3000, 4500, 6000]
LEVEL_NAMES: list[str] = ["Bamboo Grove", "Mountain Pass", "Mutant Lair"]
FLOOR_Y: int = 490

# --- Game States ---
ST_MENU = "MENU"
ST_PLAYING = "PLAYING"
ST_PAUSED = "PAUSED"
ST_GAME_OVER = "GAME_OVER"
ST_VICTORY = "VICTORY"
ST_LEVEL_TRANS = "LEVEL_TRANS"

# --- Paths ---
# PyInstaller bundles files into a temp _MEIPASS dir; use it if available
if getattr(sys, "frozen", False):
    BASE_DIR: str = sys._MEIPASS  # type: ignore[attr-defined]
else:
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
# Save file goes next to the exe (or script), not in temp dir
_EXE_DIR: str = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else BASE_DIR
SAVE_FILE: str = os.path.join(_EXE_DIR, "highscores.json")
MUTANT_PNG: str = os.path.join(BASE_DIR, "mutant.png")
