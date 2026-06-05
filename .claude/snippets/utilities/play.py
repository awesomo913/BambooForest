# From: audio.py:197
# Play a sound with 30% volume cap + rate limiting.

    def play(self, name: str) -> None:
        """Play a sound with 30% volume cap + rate limiting."""
        if not self.enabled or name not in self.sounds:
            return
        now = pygame.time.get_ticks() / 1000.0
        last = self._last_play_time.get(name, -999.0)
        elapsed = now - last
        min_gap = _MIN_INTERVAL.get(name, _DEFAULT_INTERVAL)
        if elapsed < min_gap:
            return
        sound = self.sounds[name]
        # Soft ambient volume. Rapid plays get additional 70% reduction
        # (0.3 * 0.7 = 0.21) so they don't stack harshly.
        if elapsed < 0.2:
            sound.set_volume(_BASE_VOLUME * 0.7)
        else:
            sound.set_volume(_BASE_VOLUME)
        sound.play()
        self._last_play_time[name] = now
