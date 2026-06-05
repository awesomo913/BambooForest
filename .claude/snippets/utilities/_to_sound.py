# From: audio.py:78
# Convert sample buffer to pygame Sound.

def _to_sound(buf: array.array) -> pygame.mixer.Sound:
    """Convert sample buffer to pygame Sound."""
    return pygame.mixer.Sound(buffer=buf)
