# From: web/game.py:1482
# Async entry point for Pygbag/WASM.

async def main() -> None:
    """Async entry point for Pygbag/WASM."""
    game = Game()
    await game.run()
