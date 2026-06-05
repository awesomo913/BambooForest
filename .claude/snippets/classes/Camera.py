# From: bamboo_forest.py:118

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(800 / 2)
        x = min(0, x) # Lock left edge
        x = max(-(self.width - 800), x) # Lock right edge
        self.camera = pygame.Rect(x, 0, self.width, self.height)
