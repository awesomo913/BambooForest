# Bamboo Forest — Web Build

WebAssembly port of the desktop game, playable in any modern browser via
[Pygbag](https://pygame-web.github.io/).

## How it's deployed

On every push to `master`, the GitHub Actions workflow at
`.github/workflows/deploy.yml`:

1. Installs `pygbag==0.9.3`
2. Runs `pygbag --build main.py` from this folder
3. Uploads the output to GitHub Pages

Live site: https://awesomo913.github.io/BambooForest/
Custom domain: https://revolutionarydesigns.io/ (once DNS propagates)

## What's different from the desktop build

| File | Change |
|---|---|
| `config.py` | No `sys._MEIPASS` branch |
| `game.py` | `run()` is `async` with `await asyncio.sleep(0)` each frame |
| `game.py` | Plain display mode (no `pygame.SCALED`) |
| `game.py` | `_toggle_fullscreen()` is a no-op (browsers handle F11) |
| `main.py` | 4-line Pygbag entry point |

Everything else (sprites, levels, biomes, audio) is identical.

## Local testing

```bash
pip install pygbag
cd web
pygbag --build main.py
cd build/web
python -m http.server 8000
# Open http://localhost:8000
```

First load in a fresh browser takes 15-30 seconds (downloading Pyodide +
your game bundle). Subsequent loads are near-instant thanks to caching.
