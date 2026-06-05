# From: sprites.py:850
# Apply damage + i-frames + positional knockback.

    def take_damage(self, amount: int = PLAYER_DAMAGE,
                    source_x: float | None = None) -> bool:
        """Apply damage + i-frames + positional knockback.

        source_x: world-space x of the damage source. Player is knocked
        AWAY from this point. Defaults to current x (knocks up only).
        """
        if self.invincible_timer > 0 or self.dead:
            return False
        self.health -= amount
        self.invincible_timer = PLAYER_INVINCIBLE_SEC  # i-frames
        # Knockback: away from source, slight up-bounce
        if source_x is None:
            kb_dir = 1.0 if self.facing_right else -1.0
            # Reverse direction so player bounces off attacker
            kb_dir = -kb_dir
        else:
            kb_dir = 1.0 if self.rect.centerx >= source_x else -1.0
        self.velocity_x = 380.0 * kb_dir
        self._sub_x = 0.0
        self.velocity_y = -260.0
        self.knockback_timer = 0.25
        self.is_dashing = False
        self.is_slamming = False
        self.is_gliding = False
        self.input_locked = True  # brief loss of control
        if self.health <= 0:
            self.health = 0
            self.dead = True
        return True
