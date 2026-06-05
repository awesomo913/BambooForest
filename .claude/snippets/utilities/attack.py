# From: sprites.py:896
# Swing the bamboo staff. Returns True if attack started.

    def attack(self) -> bool:
        """Swing the bamboo staff. Returns True if attack started."""
        if (self.has_bamboo_weapon and not self.is_attacking
                and self.attack_cooldown <= 0 and not self.is_dashing):
            self.is_attacking = True
            self.attack_timer = 0.25
            self.attack_cooldown = 0.4
            return True
        return False
