# From: sprites.py:926
# Ground-slam: high downward velocity while airborne.

    def slam(self) -> bool:
        """Ground-slam: high downward velocity while airborne."""
        if self.is_on_ground or self.is_slamming:
            return False
        self.is_slamming = True
        self.velocity_y = 1200.0  # fast drop
        self.is_gliding = False
        return True
