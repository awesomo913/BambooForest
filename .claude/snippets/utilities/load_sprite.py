# From: bamboo_forest.py:10
# Loads an image if it exists, otherwise returns a colored block.

def load_sprite(filename, width, height, fallback_color):
    """Loads an image if it exists, otherwise returns a colored block."""
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        image = pygame.image.load(filepath).convert_alpha() 
        return pygame.transform.scale(image, (width, height))
    else:
        surf = pygame.Surface((width, height)).convert()
        surf.fill(fallback_color)
        return surf
