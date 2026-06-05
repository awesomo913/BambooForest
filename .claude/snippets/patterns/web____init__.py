# From: web/audio.py:112

    def __init__(self) -> None:
        self.enabled = True
        self.sounds: dict = {}
        self._last_play_time: dict[str, float] = {}
        # Web build: mixer may be unavailable. Catch ANY failure and
        # disable audio gracefully instead of crashing the whole game.
        if not hasattr(pygame, "mixer"):
            self.enabled = False
            return
        try:
            pygame.mixer.init(SAMPLE_RATE, -16, 1, 512)
            pygame.mixer.set_num_channels(16)
        except (pygame.error, AttributeError, Exception):
            self.enabled = False
            return

        try:
            self._build_sounds()
        except (pygame.error, AttributeError, Exception):
            self.enabled = False
            self.sounds = {}
            return
