# From: sprites.py:935
# Toggle glide -- consumes glide_time_remaining.

    def set_gliding(self, glide: bool) -> None:
        """Toggle glide -- consumes glide_time_remaining.

        Glide only activates while timer > 0. Timer counts down only while
        actually gliding, so one 10s pickup = 10 seconds of cumulative glide.
        """
        if (glide and self.glide_time_remaining > 0
                and not self.is_on_ground and self.velocity_y > 0
                and not self.is_slamming and not self.is_dashing):
            self.is_gliding = True
        else:
            self.is_gliding = False
