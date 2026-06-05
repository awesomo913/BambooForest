# From: audio.py:32
# Generate white noise samples.

def _noise_samples(duration: float, volume: float = 0.3) -> array.array:
    """Generate white noise samples."""
    n = int(SAMPLE_RATE * duration)
    amp = int(32767 * volume)
    return array.array("h", [random.randint(-amp, amp) for _ in range(n)])
