# From: audio.py:39
# Generate pitch sweep (linear frequency interpolation).

def _sweep_samples(f_start: float, f_end: float, duration: float,
                   volume: float = 0.5) -> array.array:
    """Generate pitch sweep (linear frequency interpolation)."""
    n = int(SAMPLE_RATE * duration)
    buf = array.array("h", [0] * n)
    phase = 0.0
    for i in range(n):
        t = i / n
        freq = f_start + (f_end - f_start) * t
        phase += 2 * math.pi * freq / SAMPLE_RATE
        buf[i] = int(32767 * volume * math.sin(phase))
    return buf
