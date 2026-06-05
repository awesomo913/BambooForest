# From: audio.py:53
# Apply attack/decay amplitude envelope in-place.

def _apply_envelope(buf: array.array, attack: float = 0.01,
                    decay: float = 0.0) -> array.array:
    """Apply attack/decay amplitude envelope in-place."""
    n = len(buf)
    attack_n = int(SAMPLE_RATE * attack)
    decay_n = int(SAMPLE_RATE * decay) if decay > 0 else 0
    result = array.array("h", [0] * n)
    for i in range(n):
        env = 1.0
        if i < attack_n and attack_n > 0:
            env = i / attack_n
        if decay_n > 0 and i >= (n - decay_n):
            env *= (n - i) / decay_n
        result[i] = int(buf[i] * env)
    return result
