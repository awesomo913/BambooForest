# From: save.py:9
# Load high scores from disk. Returns sorted list of {score, level}.

def load_high_scores() -> list[dict]:
    """Load high scores from disk. Returns sorted list of {score, level}."""
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        scores = data.get("high_scores", [])
        return sorted(scores, key=lambda s: s.get("score", 0), reverse=True)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []
