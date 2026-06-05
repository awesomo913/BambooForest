# From: save.py:37
# Return the highest saved score, or 0.

def get_best_score() -> int:
    """Return the highest saved score, or 0."""
    scores = load_high_scores()
    return scores[0]["score"] if scores else 0
