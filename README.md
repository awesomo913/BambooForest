# Bamboo Forest

A lush 2D platformer adventure starring a panda exploring magical bamboo forests and wildly varied biomes.

## Quick Start (Desktop)

```powershell
cd Desktop\AI\BambooForest
python game.py
```

Controls:
- Left/Right (or A/D): move
- Space / Up / W: jump (with coyote time + jump buffer + variable height on release)
- Shift: dash (when Dash Boots equipped)
- E / X: attack with bamboo staff (when collected)
- Down / S: ground slam
- Ctrl / Q: throw shuriken (when staff)
- R: ice spell (unlocked after first boss, uses mana)
- Esc: pause / menu

## Web Version

Built with pygbag. Open `web/build/web/index.html` in a modern browser (or use the hosted build).

Touch controls supported via overlay.

## Current State & Polish In Progress

- Many biomes with unique mechanics (reverse gravity, rising lava, ice, darkness, wind, geysers, spores, etc.)
- Power-ups: glide, dash, staff, ice magic
- Full featured: combo scoring, lives, checkpoints, bosses, saves
- Desktop + web builds kept in sync

A fleet of specialized agents are actively:
- Exploring the full system
- Fixing physics/collision (including reverse grav)
- Smoothing controls (added jump buffer + variable jump height in both builds)
- Improving gameplay, levels, visuals, audio, web parity, performance, UI
- Consolidating and closing the long list of documented bugs

See the various *BUGS_REPORT.md files for history and remaining items.

## Development

- Main: `game.py` + `sprites.py` (Player), `levels.py`, `biomes.py`, `engine.py`, `ui.py`
- Web copy lives in `web/`
- Config/tuning: `config.py`
- Procedural audio/sprites

Run smoke tests with python -c importing game/sprites after `uv pip install pygame`.

Enjoy the panda's journey through the bamboo! 

(Agents actively driving fixes and next-level upgrades as of 2026-06-24)
