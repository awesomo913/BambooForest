"""High score persistence using JSON.

Desktop: file based.
Web (Pyodide/pygbag): falls back to browser localStorage when available
  (survives refresh in the same origin). Otherwise in-memory for the session.
"""

import json
import os
from config import SAVE_FILE

MAX_SCORES: int = 5

# Web detection (pygbag / emscripten)
_IS_WEB = False
try:
    import platform
    if "emscripten" in getattr(platform, "platform", lambda: "")().lower() or "pyodide" in str(os.environ):
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
    """Load high scores. Web uses localStorage when possible."""
    if _IS_WEB:
        scores = _web_load()
        return sorted(scores, key=lambda s: s.get("score", 0), reverse=True)
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        scores = data.get("high_scores", [])
        return sorted(scores, key=lambda s: s.get("score", 0), reverse=True)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError):
        return []


def save_high_score(score: int, level_reached: int) -> bool:
    """Add score if it qualifies for top 5. Returns True if it made the list."""
    scores = load_high_scores()
    entry = {"score": score, "level": level_reached}
    scores.append(entry)
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores = scores[:MAX_SCORES]

    if _IS_WEB:
        _web_save(scores)
        made_list = len(scores) < MAX_SCORES or entry["score"] >= scores[-1]["score"]
        return made_list

    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({"high_scores": scores}, f, indent=2)
    except OSError:
        return False

    made_list = len(scores) < MAX_SCORES or entry["score"] >= scores[-1]["score"]
    return made_list


def get_best_score() -> int:
    """Return the highest saved score, or 0."""
    scores = load_high_scores()
    return scores[0]["score"] if scores else 0
