# From: sprites.py:973
# Cast an ice projectile. Requires full mana and unlock.

    def cast_ice_spell(self) -> bool:
        """Cast an ice projectile. Requires full mana and unlock.

        Returns True if cast, False if blocked (no unlock / no mana / cd).
        """
        if not self.has_ice_magic:
            return False
        if self.ice_cast_cooldown > 0:
            return False
        if self.mana < self.mana_max:
            return False
        # Consume all mana and set 10s cooldown
        self.mana = 0.0
        self.ice_cast_cooldown = 10.0
        self.pending_ice_casts.append((
            self.rect.centerx, self.rect.centery,
            1.0 if self.facing_right else -1.0))
        return True
