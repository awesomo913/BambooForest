# From: sprites.py:962
# Throw a bamboo shuriken. Returns True if thrown.

    def throw_bamboo(self) -> bool:
        """Throw a bamboo shuriken. Returns True if thrown."""
        if self.throw_cooldown > 0 or not self.has_bamboo_weapon:
            return False
        self.throw_cooldown = 0.5
        # Signal to game loop to spawn a projectile
        self.pending_throws.append((self.rect.centerx,
                                   self.rect.centery,
                                   1.0 if self.facing_right else -1.0))
        return True
