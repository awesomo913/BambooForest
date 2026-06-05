# From: sprites.py:992
# Called on level load / respawn to clear any transient locks.

    def reset_state(self) -> None:
        """Called on level load / respawn to clear any transient locks."""
        self.input_locked = False
        self.is_attacking = False
        self.is_dashing = False
        self.is_wall_sliding = False
        self.is_slamming = False
        self.is_gliding = False
        self.attack_timer = 0.0
        self.attack_cooldown = 0.0
        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.throw_cooldown = 0.0
        self.pending_throws = []
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self._sub_x = 0.0
        self.gravity_multiplier = 1.0
        # Ice magic: reset cooldown + pending cast list, keep has_ice_magic
        self.ice_cast_cooldown = 0.0
        self.pending_ice_casts = []
