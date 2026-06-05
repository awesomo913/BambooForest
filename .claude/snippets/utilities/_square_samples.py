# From: audio.py:21
# Generate square wave samples.

def _square_samples(freq: float, duration: float, volume: float = 0.3) -> array.array:
    """Generate square wave samples."""
    n = int(SAMPLE_RATE * duration)
    period = SAMPLE_RATE / freq if freq > 0 else SAMPLE_RATE
    buf = array.array("h", [0] * n)
    for i in range(n):
        val = 1 if (i % int(period)) < (period / 2) else -1
        buf[i] = int(32767 * volume * val)
    return buf
