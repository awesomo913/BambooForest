# From: module_auto.py:15

def load_image(filename):
    try:
        return pygame.image.load(filename).convert_alpha()
    except FileNotFoundError:
        print(f"Error: No file '{filename}' found in working directory.")
        return None
