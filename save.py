"""High score persistence using JSON (profile).

Desktop: writes <game>/highscores.json
Web (Pyodide/pygbag via pygbag): uses browser localStorage "bambooforest_profile"
  (survives refresh). Direct FS open() is unreliable under WASM (pyodide FS
  often in-memory only or needs IDBFS mount + sync); we route all web I/O
  through localStorage to avoid silent fails reported in prior runs.

Versioned saves (current: 2). Old plain {"high_scores": [...]} files are
auto-migrated on load.

Cloud / backup:
- Desktop: copy the highscores.json file next to the game.
- Web: DevTools → Application → Local Storage (origin) → copy the value of
  key "bambooforest_profile" (or use JSON export). Paste back to restore.
No built-in cloud sync.

Unlocks (ice magic, glide, ...) and other meta are persisted with the profile.
"""

import json
import os
import sys
from config import SAVE_FILE, DEFAULT_ACCESSIBILITY

MAX_SCORES: int = 5
SAVE_VERSION: int = 2

# Web detection (pygbag / emscripten / pyodide)
_IS_WEB = False
try:
    if ("pyodide" in sys.modules or
        "js" in sys.modules or
        getattr(sys, "platform", "") == "emscripten" or
        "emscripten" in os.environ.get("PYTHONPATH", "") or
        "pyodide" in str(os.environ) or
        "emscripten" in str(getattr(__import__("platform", fromlist=[""]), "platform", lambda: "")()).lower()):
        _IS_WEB = True
except Exception:
    pass

_web_scores = None  # session fallback


def _web_load():
    global _web_scores
    if _web_scores is not None:
        return _web_scores
    try:
        from js import localStorage  # type: ignore
        raw = localStorage.getItem("bambooforest_highscores")
        if raw:
            data = json.loads(raw)
            _web_scores = data.get("high_scores", [])
            return _web_scores
    except Exception:
        pass
    _web_scores = []
    return _web_scores


def _web_save(scores):
    global _web_scores
    _web_scores = scores
    try:
        from js import localStorage  # type: ignore
        localStorage.setItem("bambooforest_highscores", json.dumps({"high_scores": scores}))
    except Exception:
        pass  # in-memory only this session


def load_high_scores() -> list[dict]:
    """Load high scores from unified profile (high_scores + settings)."""
    data = _load_profile_data()
    scores = data.get("high_scores", [])
    return sorted(scores, key=lambda s: s.get("score", 0), reverse=True) if scores else []


def save_high_score(score: int, level_reached: int) -> bool:
    """Add score if it qualifies for top 5. Persists in profile."""
    data = _load_profile_data()
    scores = data.get("high_scores", [])
    entry = {"score": score, "level": level_reached}
    scores.append(entry)
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores = scores[:MAX_SCORES]
    data["high_scores"] = scores
    ok = _save_profile_data(data)
    made = (len(scores) < MAX_SCORES or entry["score"] >= scores[-1]["score"]) if scores else True
    return ok and made


# ---------------------------------------------------------------------------
# Grove meta: essences (per biome) + grafts (player modifiers)
# Stored in the unified profile alongside high_scores + settings.
# ---------------------------------------------------------------------------

ESSENCE_BIOME_KEYS: list[str] = [
    "forest", "corrupted", "lair", "volcanic", "basalt", "desert",
    "cave", "salt", "mushroom", "forge", "tidal", "void", "gravity",
]

DEFAULT_ESSENCES: dict[str, int] = {k: 0 for k in ESSENCE_BIOME_KEYS}
DEFAULT_GRAFTS: list[str] = []


def load_essences() -> dict[str, int]:
    """Return essences counts (biome -> count)."""
    data = _load_profile_data()
    ess = data.get("essences", {}).copy()
    for k in ESSENCE_BIOME_KEYS:
        ess.setdefault(k, 0)
    return ess


def add_essence(biome: str) -> dict[str, int]:
    """Award +1 essence for the biome key. Persists. Returns new counts."""
    if biome not in ESSENCE_BIOME_KEYS:
        biome = "forest"
    data = _load_profile_data()
    ess = data.get("essences", {}).copy()
    for k in ESSENCE_BIOME_KEYS:
        ess.setdefault(k, 0)
    ess[biome] = ess.get(biome, 0) + 1
    data["essences"] = ess
    _save_profile_data(data)
    return ess


def spend_essence(n: int = 1) -> int:
    """Consume up to n essence from any biomes (for light Grove purchases).
    Returns actual number spent (0 if none available). Persists.
    """
    if n <= 0:
        return 0
    data = _load_profile_data()
    ess = data.get("essences", {}).copy()
    for k in ESSENCE_BIOME_KEYS:
        ess.setdefault(k, 0)
    remaining = n
    spent = 0
    for k in list(ess.keys()):
        if remaining <= 0:
            break
        take = min(ess.get(k, 0), remaining)
        if take > 0:
            ess[k] -= take
            spent += take
            remaining -= take
    data["essences"] = ess
    _save_profile_data(data)
    return spent


def spend_specific_essences(essence_keys: list[str]) -> bool:
    """Spend exactly 1 of each provided biome essence key (for 2-3 combine bench).
    Returns True only if every key had >=1 and all were decremented. Persists.
    """
    if not essence_keys or len(essence_keys) < 2 or len(essence_keys) > 3:
        return False
    data = _load_profile_data()
    ess = data.get("essences", {}).copy()
    for k in ESSENCE_BIOME_KEYS:
        ess.setdefault(k, 0)
    # verify availability (exact match, no over-spend)
    for ek in essence_keys:
        if ek not in ESSENCE_BIOME_KEYS or ess.get(ek, 0) < 1:
            return False
    # commit spend
    for ek in essence_keys:
        ess[ek] -= 1
    data["essences"] = ess
    return _save_profile_data(data)


def load_grafts() -> list[str]:
    """Return list of unlocked graft ids."""
    data = _load_profile_data()
    return list(data.get("grafts", []))


def unlock_graft(graft_id: str) -> bool:
    """Add graft if new. Persists. Returns True if newly added."""
    data = _load_profile_data()
    grafts = list(data.get("grafts", []))
    if graft_id in grafts:
        return False
    grafts.append(graft_id)
    data["grafts"] = grafts
    return _save_profile_data(data)


def get_profile_essences_and_grafts() -> tuple[dict[str, int], list[str]]:
    """Convenience: return (essences, grafts) snapshot."""
    data = _load_profile_data()
    ess = data.get("essences", {}).copy()
    for k in ESSENCE_BIOME_KEYS:
        ess.setdefault(k, 0)
    gr = list(data.get("grafts", []))
    return ess, gr


# ---------------------------------------------------------------------------
# Permanent unlocks (ice magic from boss, glide once collected, etc.)
# Stored under "unlocks": {"ice": true, "glide": true, ...}
# These are set on first achievement and survive deaths + level transitions.
# ---------------------------------------------------------------------------

DEFAULT_UNLOCKS: dict[str, bool] = {"ice": False, "glide": False, "overgrown": False}


def load_unlocks() -> dict[str, bool]:
    """Return current permanent unlocks (defaults false for unknown keys)."""
    data = _load_profile_data()
    u = data.get("unlocks", {})
    out = DEFAULT_UNLOCKS.copy()
    for k in DEFAULT_UNLOCKS:
        if k in u:
            out[k] = bool(u[k])
    return out


def save_unlock(key: str, value: bool = True) -> bool:
    """Persist a single unlock flag. Creates key if new. Returns success."""
    if key not in DEFAULT_UNLOCKS:
        # allow future keys but normalize
        pass
    data = _load_profile_data()
    unlocks = data.get("unlocks", {}).copy()
    unlocks[key] = bool(value)
    data["unlocks"] = unlocks
    data["version"] = SAVE_VERSION
    return _save_profile_data(data)


def save_unlocks(unlocks: dict[str, bool]) -> bool:
    """Persist multiple unlock flags at once (used on deaths/wins for reliability)."""
    data = _load_profile_data()
    cur = data.get("unlocks", {}).copy()
    for k, v in unlocks.items():
        cur[k] = bool(v)
    data["unlocks"] = cur
    data["version"] = SAVE_VERSION
    return _save_profile_data(data)


def get_best_score() -> int:
    """Return the highest saved score, or 0."""
    scores = load_high_scores()
    return scores[0]["score"] if scores else 0


# ---------------------------------------------------------------------------
# Profile / Accessibility settings (persisted with high scores)
# ---------------------------------------------------------------------------

DEFAULT_SETTINGS = DEFAULT_ACCESSIBILITY.copy()


def _load_profile_data():
    """Return full profile dict (high_scores + settings + unlocks + version). Web-aware.

    Migrates legacy plain high score JSONs and ensures version + unlocks keys.
    """
    if _IS_WEB:
        try:
            from js import localStorage  # type: ignore
            raw = localStorage.getItem("bambooforest_profile")
            if raw:
                data = json.loads(raw)
                if isinstance(data, dict):
                    return _migrate_profile(data)
        except Exception as e:
            # Pyodide/JS access can fail in some embed contexts; fall back
            pass
        return {"version": SAVE_VERSION, "high_scores": [], "settings": DEFAULT_SETTINGS.copy(), "unlocks": {}, "bests": {"times": {}, "ghosts": {}}}
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            data = {}
        return _migrate_profile(data)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError, TypeError):
        return {"version": SAVE_VERSION, "high_scores": [], "settings": DEFAULT_SETTINGS.copy(), "unlocks": {}, "bests": {"times": {}, "ghosts": {}}}


def _migrate_profile(data: dict) -> dict:
    """Ensure keys and bump version. Safe for old files."""
    if not isinstance(data, dict):
        data = {}
    data.setdefault("version", 1)
    data.setdefault("high_scores", [])
    data.setdefault("settings", DEFAULT_SETTINGS.copy())
    data.setdefault("unlocks", {})
    data.setdefault("bests", {"times": {}, "ghosts": {}})
    # If old top-level only scores existed in some builds, keep as-is (profile already wrapped)
    if data.get("version", 1) < SAVE_VERSION:
        data["version"] = SAVE_VERSION
    return data


def _save_profile_data(data: dict) -> bool:
    """Write full profile. Web-aware. Returns success. Hardened against silent FS fails."""
    data = dict(data)  # copy
    data["version"] = SAVE_VERSION
    if _IS_WEB:
        try:
            from js import localStorage  # type: ignore
            localStorage.setItem("bambooforest_profile", json.dumps(data))
            return True
        except Exception as e:
            # Common pyodide case: no window / no LS in this context.
            # Caller gets False so it can decide (e.g. keep in mem for session).
            # Do not swallow without trace in debug; here we surface via return.
            return False
    try:
        # Desktop: ensure dir exists (in case SAVE_FILE is in frozen exe dir)
        d = os.path.dirname(SAVE_FILE)
        if d and not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except (OSError, PermissionError, IOError) as e:
        # Report-ish: avoid total silent fail. In real app could route to crash_logger.
        try:
            print(f"[save] WARNING: failed writing profile to {SAVE_FILE}: {e}", file=sys.stderr)
        except Exception:
            pass
        return False


def load_settings() -> dict:
    """Load accessibility settings (merged with defaults for safety)."""
    data = _load_profile_data()
    settings = data.get("settings", {}).copy()
    # Merge missing keys with defaults (forward compat)
    for k, v in DEFAULT_SETTINGS.items():
        if k not in settings:
            settings[k] = v
    # Clamp to known sane values (support legacy keys from prior stubs for migration)
    pd = settings.get("particle_density", settings.get("particle_intensity", 1.0))
    settings["particle_density"] = max(0.5, min(1.5, float(pd)))
    si = settings.get("shake_intensity", settings.get("shake_scale", 1.0))
    settings["shake_intensity"] = max(0.5, min(1.5, float(si)))
    settings["text_scale"] = max(0.5, min(2.0, float(settings.get("text_scale", 1.0))))
    settings["reduced_motion"] = bool(settings.get("reduced_motion", False))
    settings["color_filter"] = max(0, min(4, int(settings.get("color_filter", 0))))
    settings["game_speed"] = max(0.5, min(1.5, float(settings.get("game_speed", 1.0))))
    return settings


def save_settings(settings: dict) -> bool:
    """Persist settings (keeps high scores)."""
    data = _load_profile_data()
    data["settings"] = {k: settings.get(k, DEFAULT_SETTINGS[k]) for k in DEFAULT_SETTINGS}
    return _save_profile_data(data)


# ---------------------------------------------------------------------------
# Speedrun bests: per-level best time + lightweight ghost (pos + facing samples)
# Stored under "bests": {"times": {"0": 42.3, ...}, "ghosts": {"0": [[t,x,y,facing], ...]}}
# ---------------------------------------------------------------------------

def _ensure_bests(data: dict) -> None:
    if "bests" not in data or not isinstance(data["bests"], dict):
        data["bests"] = {"times": {}, "ghosts": {}}
    data["bests"].setdefault("times", {})
    data["bests"].setdefault("ghosts", {})


def load_best_time(level: int) -> float | None:
    """Return best time for level (seconds) or None."""
    data = _load_profile_data()
    _ensure_bests(data)
    t = data["bests"]["times"].get(str(level))
    return float(t) if t is not None else None


def save_best_run(level: int, time_sec: float, ghost: list) -> bool:
    """Save if better (or first). Stores time + ghost samples. Returns True if saved."""
    data = _load_profile_data()
    _ensure_bests(data)
    key = str(level)
    prev = data["bests"]["times"].get(key)
    if prev is not None and float(prev) <= time_sec:
        return False  # not better
    data["bests"]["times"][key] = round(float(time_sec), 3)
    # store compact ghost
    data["bests"]["ghosts"][key] = [[round(float(s[0]), 3), int(s[1]), int(s[2]), bool(s[3])] for s in ghost]
    return _save_profile_data(data)


def get_best_ghost(level: int) -> list | None:
    """Return list of [t, x, y, facing] or None."""
    data = _load_profile_data()
    _ensure_bests(data)
    g = data["bests"]["ghosts"].get(str(level))
    if not g:
        return None
    # normalize shape
    return [[float(s[0]), int(s[1]), int(s[2]), bool(s[3])] for s in g]


def get_best_time(level: int) -> float | None:
    """Alias for load_best_time (convenience)."""
    return load_best_time(level)


# ---------------------------------------------------------------------------
# Daily challenge completion tracking + best times (expanded to full modifiers)
# "daily_completions": {"20260624": true, ...}
# "daily_bests": {"20260624": 1234.56, ...}  # best full-run clear time (sec) for seed
# ---------------------------------------------------------------------------

def mark_daily_complete(daily_seed: int) -> bool:
    """Mark this daily seed completed (on victory in daily mode). Persists."""
    data = _load_profile_data()
    dailies = data.setdefault("daily_completions", {})
    dailies[str(daily_seed)] = True
    return _save_profile_data(data)


def is_daily_complete(daily_seed: int) -> bool:
    """Return True if this daily seed (YYYYMMDD) was completed."""
    data = _load_profile_data()
    dailies = data.get("daily_completions", {})
    return bool(dailies.get(str(daily_seed), False))


def save_daily_best(daily_seed: int, time_sec: float) -> bool:
    """Save best full-run daily time for seed if improved (or first). Also marks complete. Persists."""
    data = _load_profile_data()
    dbests = data.setdefault("daily_bests", {})
    key = str(daily_seed)
    prev = dbests.get(key)
    if prev is not None and float(prev) <= float(time_sec):
        return False
    dbests[key] = round(float(time_sec), 3)
    data.setdefault("daily_completions", {})[key] = True
    return _save_profile_data(data)


def get_daily_best(daily_seed: int) -> float | None:
    """Return best full daily run time in seconds, or None."""
    data = _load_profile_data()
    dbests = data.get("daily_bests", {})
    t = dbests.get(str(daily_seed))
    return float(t) if t is not None else None


# ---------------------------------------------------------------------------
# Overgrown post-game challenge unlock (basic post-game area)
# Stored under unlocks["overgrown"] = true. Set on L18 victory + high essence.
# ---------------------------------------------------------------------------

def is_overgrown_unlocked() -> bool:
    """Return True if post-game Overgrown challenge is unlocked."""
    data = _load_profile_data()
    u = data.get("unlocks", {})
    return bool(u.get("overgrown", False))


def unlock_overgrown() -> bool:
    """Set the overgrown unlock flag. Returns success."""
    return save_unlock("overgrown")


# (high score load/save now implemented above using the profile helpers for unified persistence)
