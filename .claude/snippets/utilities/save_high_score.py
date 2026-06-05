# From: save.py:20
# Add score if it qualifies for top 5. Returns True if it made the list.

def save_high_score(score: int, level_reached: int) -> bool:
    """Add score if it qualifies for top 5. Returns True if it made the list."""
    scores = load_high_scores()
    entry = {"score": score, "level": level_reached}
    scores.append(entry)
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores = scores[:MAX_SCORES]

    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({"high_scores": scores}, f, indent=2)
    except OSError:
        return False

    return entry in scores
