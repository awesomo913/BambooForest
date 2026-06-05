# From: engine.py:20
# Smooth-follow camera. Logic state is float, render state is int.

class Camera:
    """Smooth-follow camera. Logic state is float, render state is int.

    offset_x / offset_y: float -- smooth lerp tracking (logic camera).
    render_x / render_y: int   -- math.floor of offset (render camera).

    All sprites and tiles are drawn relative to render_x/render_y,
    which locks everything to the same integer pixel grid.
    """

    def __init__(self, world_width: int, world_height: int) -> None:
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0
        self.render_x: int = 0
        self.render_y: int = 0
        self.world_width = world_width
        self.world_height = world_height

    def update(self, target: pygame.sprite.Sprite, dt: float) -> None:
        # Lock camera directly to player -- no lerp, no float drift.
        # Player rect is always integer, so goal is always integer,
        # which means offset is always integer. Zero sub-pixel jitter.
        goal_x = -target.rect.centerx + SCREEN_WIDTH // 2
        goal_y = -target.rect.centery + SCREEN_HEIGHT // 2
        self.offset_x = float(max(-(self.world_width - SCREEN_WIDTH), min(0, goal_x)))
        self.offset_y = float(max(-(self.world_height - SCREEN_HEIGHT), min(0, goal_y)))
        self.render_x = math.floor(self.offset_x)
        self.render_y = math.floor(self.offset_y)

    def apply(self, entity: pygame.sprite.Sprite) -> pygame.Rect:
        return entity.rect.move(math.floor(self.offset_x), math.floor(self.offset_y))

    def apply_pos(self, x: float, y: float) -> tuple[float, float]:
        return (x + self.offset_x, y + self.offset_y)

    def get_visible_rect(self) -> pygame.Rect:
        return pygame.Rect(-self.render_x, -self.render_y, SCREEN_WIDTH, SCREEN_HEIGHT)
