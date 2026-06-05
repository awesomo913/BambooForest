# From: sprites.py:948
# Legacy accessor -- returns True if player currently has glide time.

    @property
    def has_glide(self) -> bool:
        """Legacy accessor -- returns True if player currently has glide time."""
        return self.glide_time_remaining > 0
