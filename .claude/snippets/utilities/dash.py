# From: sprites.py:906
# SHIFT-key dash. Requires DashBoots pickup (timed item).

    def dash(self) -> bool:
        """SHIFT-key dash. Requires DashBoots pickup (timed item).

        Pickup grants dash_time_remaining > 0 for a limited duration.
        Player can still dash freely during that window, subject to the
        normal 700ms cooldown between dashes.
        """
        if self.dash_time_remaining <= 0:
            return False  # no dash boots equipped
        if self.is_dashing or self.dash_cooldown > 0:
            return False
        self.is_dashing = True
        self.dash_timer = 0.18
        self.dash_cooldown = 0.7
        self.input_locked = True
        self.invincible_timer = max(self.invincible_timer, 0.2)
        self.dash_direction = 1.0 if self.facing_right else -1.0
        self.velocity_x = 900.0 * self.dash_direction
        return True
