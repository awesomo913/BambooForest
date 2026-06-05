# From: engine.py:85

class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color",
                 "size", "shape", "gravity")

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 life: float, color: tuple, size: float,
                 shape: str = "circle", gravity: bool = False) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
        self.shape = shape
        self.gravity = gravity
