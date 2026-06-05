# From: audio.py:12
# Generate signed-16-bit sine wave samples.

def _sine_samples(freq: float, duration: float, volume: float = 0.5) -> array.array:
    """Generate signed-16-bit sine wave samples."""
    n = int(SAMPLE_RATE * duration)
    buf = array.array("h", [0] * n)
    for i in range(n):
        buf[i] = int(32767 * volume * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))
    return buf
