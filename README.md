# Bamboo Forest

A lush 2D platformer. Play as a panda collecting bamboo across 18 themed levels with changing rules, enemies, and power-ups. Distinct biomes, power-ups (glide, dash, staff, ice), scoring, and high scores.

**Last updated:** 2026-06-24

## Zero-Friction Run (Desktop)
```powershell
# From the BambooForest folder (clone the repo)
uv pip install -r requirements.txt
python game.py
```

That's it. No other setup. Game uses only pygame + stdlib.

## Controls
- Arrow keys or A/D + W or Space/Up: move and jump (variable height on release, coyote time + jump buffer).
- SHIFT: dash (with Dash Boots).
- E or X or mouse click: attack with staff (with Bamboo Staff).
- Down/S: ground slam.
- Ctrl/Q: throw bamboo shuriken.
- R: cast ice spell (unlocked after first boss).
- F11: fullscreen. ESC: pause/menu. G: The Grove (from title or pause). TAB: debug (dev).

## Web Version
See `web/README.md` for pygbag build and local test. Live at the GitHub Pages link in the repo (https://awesomo913.github.io/BambooForest/ or equivalent).

Local web test after build:
```powershell
cd web
python -m http.server 8000 -d build/web
# open http://localhost:8000
```

## Packaging & Sharing
- `requirements.txt` + `pyproject.toml` for modern `uv` / pip workflows.
- Desktop run as above.
- For exe (PyInstaller): use existing .spec if present, or `pyinstaller game.py`.
- High scores persist locally (desktop file + browser localStorage on web).
- Clean tree: run `git status` — no __pycache__, build/, *.exe, highscores, or web/build artifacts should be tracked.

## Current State & Polish
- 18 levels, biome-specific mechanics (geysers, crumbling, wind, ice friction, rising lava, gravity flip, portals, darkness crystals, etc.).
- Power-ups, permanent unlocks (ice after boss), combo scoring, lives, checkpoints.
- Desktop + web builds with ongoing parity work.
- Recent agent-driven improvements: smoother controls (jump buffer, variable height, reverse-grav support), juicy feedback, UI polish (icons, pills, touch targets), better persistence, docs, packaging.

See:
- `BREAKDOWN.md` for architecture.
- `TUTORIAL.md` for play guide + recipes.
- `HANDOFF.md`, `PROOF.md` for full context.
- Bug reports (MASTER_GLITCH, PHYSICS, etc.) for tracked issues being fixed by the swarm.

High scores saved locally. Collect bamboo to earn biome essences; visit The Grove (G) from title/pause to combine 2 into passive grafts (glide, dash, lava tweaks) that persist in your profile.

## Dev Notes
- Main entry: `python game.py` (or `game:main` via packaging).
- Web entry: `web/main.py` (pygbag).
- All changes keep desktop/web in sync where possible.
- `.gitignore` keeps build junk out of git.

First-time experience: clone → uv pip install -r requirements.txt → python game.py. Done.
