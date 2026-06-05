# From: game.py:170
# Grant ice magic on first boss defeat. Persists across levels.

    def _maybe_unlock_ice_magic(self) -> None:
        """Grant ice magic on first boss defeat. Persists across levels."""
        if self._has_ice_magic_permanent:
            return
        self._has_ice_magic_permanent = True
        self.player.has_ice_magic = True
        self.player.mana = self.player.mana_max  # full mana as reward
        self._ice_tutorial_timer = 999.0
        self._ice_used = False
        self.hud.add_floating_text(
            "ICE MAGIC UNLOCKED!",
            self.player.rect.centerx, self.player.rect.top - 40,
            (140, 220, 255))
        # Big sparkle burst around player
        for _ in range(20):
            self.particles.emit_sparkle(
                self.player.rect.centerx,
                self.player.rect.centery, 1)
        self.audio.play("crystal")
