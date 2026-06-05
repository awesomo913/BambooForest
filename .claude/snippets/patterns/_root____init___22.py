# From: biomes.py:767

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((34, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (80, 60, 60), (10, 8, 14, 16))
        pygame.draw.polygon(self.image, (100, 70, 70), [(10, 14), (0, 4), (14, 10)])
        pygame.draw.polygon(self.image, (100, 70, 70), [(24, 14), (34, 4), (20, 10)])
        pygame.draw.circle(self.image, (255, 120, 40), (14, 13), 2)
        pygame.draw.circle(self.image, (255, 120, 40), (20, 13), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.state = "hover"
        self.swoop_tx: float = 0.0
        self.swoop_ty: float = 0.0
        self.alive_flag = True
        self.hover_timer: float = 0.0
