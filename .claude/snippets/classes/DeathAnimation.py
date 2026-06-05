# From: ui.py:866

class DeathAnimation:
    def __init__(self) -> None:
        self.timer: float = 1.0
        self.time_scale: float = 0.3

    def update(self, dt: float) -> bool:
        self.timer -= dt
        return self.timer <= 0

    def get_time_scale(self) -> float:
        return self.time_scale
