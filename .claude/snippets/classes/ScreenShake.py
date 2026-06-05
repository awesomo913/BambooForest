# From: engine.py:63

class ScreenShake:
    def __init__(self) -> None:
        self.timer: float = 0.0
        self.intensity: int = 0

    def trigger(self, intensity: int = SHAKE_INTENSITY,
                duration: float = SHAKE_DURATION) -> None:
        self.timer = duration
        self.intensity = intensity

    def update(self, dt: float) -> tuple[int, int]:
        if self.timer > 0:
            self.timer -= dt
            return (random.randint(-self.intensity, self.intensity),
                    random.randint(-self.intensity, self.intensity))
        return (0, 0)
