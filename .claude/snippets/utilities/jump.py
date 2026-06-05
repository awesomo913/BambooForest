# From: sprites.py:830
# Jump the player. Honors coyote time (0.12s window after leaving

    def jump(self) -> bool:
        """Jump the player. Honors coyote time (0.12s window after leaving
        ground) so platform-separation jitter doesn't silently eat jumps."""
        # If we just walked off a ledge / a moving platform just dropped
        # away, jumps_remaining may have been decremented to 0 by an earlier
        # mid-air double-jump even though we're technically still "groundable".
        # Coyote time rescues us by restoring a ground-jump.
        if self.coyote_timer > 0 and self.jumps_remaining < (
                2 if self.has_double_jump else 1):
            # Consume coyote to give back the ground-jump
            self.jumps_remaining = 2 if self.has_double_jump else 1
            self.coyote_timer = 0.0
        if self.jumps_remaining > 0:
            self.velocity_y = PLAYER_JUMP
            self.jumps_remaining -= 1
            if self.is_on_ground:
                self.is_on_ground = False
            return True
        return False
