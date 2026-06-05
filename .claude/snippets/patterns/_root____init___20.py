# From: biomes.py:682

    def __init__(self, x: int, y: int, direction: float) -> None:
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 180, 60), (4, 4), 4)
        self.rect = self.image.get_rect(center=(x, y))
        angle = math.radians(45)
        self.vx = SCORPION_PROJ_SPEED * direction * math.cos(angle)
        self.vy = -SCORPION_PROJ_SPEED * math.sin(angle)
        self.pos_x = float(x)
        self.pos_y = float(y)
