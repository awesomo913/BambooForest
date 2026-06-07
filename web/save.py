"""High score persistence using JSON (WASM-aware).

On desktop: writes to JSON file on disk.
On WASM/Pyodide: writes to window.localStorage (browser storage).
"""

import json
import sys
from config import SAVE_FILE

MAX_SCORES: int = 5

_IS_WASM = sys.platform == "emscripten"


def _get_storage():
    """Lazy-import js module for WASM. Returns None on desktop."""
    if _IS_WASM:
        try:
            from js import localStorage  # type: ignore
            return localStorage
        except ImportError:
            return None
    return None


def load_high_scores() -> list[dict]:
    """Load high scores. Returns sorted list of {score, level}."""
    raw: str | None = None
    if _IS_WASM:
        store = _get_storage()
        if store is not None:
            raw = store.getItem("bamboo_high_scores") or None
    else:
        try:
            with open(SAVE_FILE, "r") as f:
                raw = f.read()
        except (FileNotFoundError, OSError):
            pass

    if raw:
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                scores = data.get("high_scores", [])
            elif isinstance(data, list):
                scores = data
            else:
                scores = []
            return sorted(scores, key=lambda s: s.get("score", 0), reverse=True)
        except (json.JSONDecodeError, KeyError):
            pass
    return []


def save_high_score(score: int, level_reached: int) -> bool:
    """Add score if it qualifies for top 5. Returns True if it made the list."""
    scores = load_high_scores()
    entry = {"score": score, "level": level_reached}
    scores.append(entry)
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores = scores[:MAX_SCORES]

    # Check if entry made the cut BEFORE the ranked check
    made_list = len(scores) < MAX_SCORES or entry["score"] >= scores[-1]["score"]

    data = json.dumps({"high_scores": scores})

    if _IS_WASM:
        store = _get_storage()
        if store is not None:
            store.setItem("bamboo_high_scores", data)
            return made_list
        return False

    try:
        with open(SAVE_FILE, "w") as f:
            f.write(data)
    except OSError:
        return False

    return made_list


def get_best_score() -> int:
    """Return the highest saved score, or 0."""
    scores = load_high_scores()
    return scores[0]["score"] if scores else 0
