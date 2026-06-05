<!-- claude-backend:generated:start -->
# BambooForest

## Overview

- **Files**: 33 (.py (25), .md (8))
- **Entry points**: `bamboo_app.py`, `bamboo_forest.py`, `game.py`, `module_auto.py`, `Bamboo_Game/bamboo_app.py`
- **Key files**: `CLAUDE.md`, `.gitignore`

## Structure

```
Bamboo_Game/  (1 files)
web/  (12 files)
```

## Conventions

- Use `os.path` for path operations (legacy style)
- Type hints are used extensively -- maintain them
- Use specific exception types in except clauses
- Uses print() for output (consider migrating to logging)
- Absolute imports preferred

## Modules

- `Bamboo_Game/bamboo_app.py` [entry]
- `audio.py` -- Procedural sound effect generation via WAV synthesis
- `backgrounds.py` -- Biome-themed parallax backgrounds
- `bamboo_app.py` [entry]
- `bamboo_forest.py` [entry]
- `biomes.py` -- Biome-specific sprites: mechanics, enemies, NPCs for levels 4-8
- `config.py` -- All game constants, colors, and tuning parameters
- `engine.py` -- Camera, particle system, parallax background, and screen shake
- `game.py` -- Bamboo Forest - Main game entry point and loop [entry]
- `levels.py` -- Level definitions and construction
- `module_auto.py` [entry]
- `save.py` -- High score persistence using JSON
- `sprites.py` -- All sprite classes and procedural pixel-art generators
- `ui.py` -- Title screen, HUD, transitions, and overlays
- `web/audio.py` -- Procedural sound effect generation via WAV synthesis
- `web/backgrounds.py` -- Biome-themed parallax backgrounds
- `web/biomes.py` -- Biome-specific sprites: mechanics, enemies, NPCs for levels 4-8
- `web/config.py` -- All game constants, colors, and tuning parameters
- `web/engine.py` -- Camera, particle system, parallax background, and screen shake
- `web/game.py` -- Bamboo Forest - Main game entry point and loop (WEB BUILD) [entry]
- `web/levels.py` -- Level definitions and construction
- `web/main.py` -- Pygbag entry point -- delegates to game.main()
- `web/save.py` -- High score persistence using JSON
- `web/sprites.py` -- All sprite classes and procedural pixel-art generators
- `web/ui.py` -- Title screen, HUD, transitions, and overlays

## Snippets

See `.claude/snippets/INDEX.md` for reusable code blocks.

<!-- claude-backend:generated:end -->
