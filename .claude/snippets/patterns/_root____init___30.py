# From: biomes.py:1265

    def __init__(self, x: int, y: int, name: str,
                 dialog: list[str], color: tuple) -> None:
        super().__init__()
        self.image = pygame.Surface((32, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, (2, 4, 28, 32))
        pygame.draw.circle(self.image, color, (16, 8), 10)
        pygame.draw.circle(self.image, COL_WHITE, (12, 7), 3)
        pygame.draw.circle(self.image, COL_WHITE, (20, 7), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 7), 2)
        pygame.draw.circle(self.image, COL_BLACK, (19, 7), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.name = name
        self.dialog_lines = dialog
        self.current_line = 0
        self.show_dialog = False
