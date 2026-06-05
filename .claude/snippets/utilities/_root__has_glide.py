# From: sprites.py:953
# Legacy setter -- grants 10s of glide or clears timer.

    @has_glide.setter
    def has_glide(self, value: bool) -> None:
        """Legacy setter -- grants 10s of glide or clears timer."""
        from config import GLIDE_DURATION_SEC
        if value:
            self.glide_time_remaining = GLIDE_DURATION_SEC
        else:
            self.glide_time_remaining = 0.0
