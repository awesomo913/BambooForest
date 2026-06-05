# From: engine.py:30

    def __init__(self, world_width: int, world_height: int) -> None:
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0
        self.render_x: int = 0
        self.render_y: int = 0
        self.world_width = world_width
        self.world_height = world_height
