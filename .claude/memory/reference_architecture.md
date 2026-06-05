---
name: BambooForest Architecture
description: Module map and dependency graph for BambooForest
type: reference
---

# BambooForest Architecture

## (root)/

- `audio.py`: Procedural sound effect generation via WAV synthesis. | exports: SAMPLE_RATE, AudioManager
- `backgrounds.py`: Biome-themed parallax backgrounds. | exports: ForestBackground, VolcanicBackground, BasaltBackground, DesertBackground, CaveBackground, SaltFlatsBackground, MushroomBackground, TidalBackground
- `bamboo_app.py` | exports: Panda, Bamboo, MutantPanda, main
- `bamboo_forest.py` | exports: BASE_DIR, load_sprite, Panda, Platform, Bamboo, HealingItem, MutantPanda, Camera
- `biomes.py`: Biome-specific sprites: mechanics, enemies, NPCs for levels 4-8. | exports: generate_volcanic_tile, generate_basalt_tile, generate_sandstone_tile, generate_limestone_tile, generate_salt_tile, generate_mushroom_tile, generate_tidal_tile, generate_gravity_tile
- `config.py`: All game constants, colors, and tuning parameters. | exports: COL_SKY, COL_PANDA_BLACK, COL_PANDA_WHITE, COL_BAMBOO, COL_BAMBOO_JOINT, COL_PLAT_GRASS, COL_PLAT_DIRT, COL_HEAL_PINK
- `engine.py`: Camera, particle system, parallax background, and screen shake. | exports: Camera, ScreenShake, Particle, ParticleSystem, ParallaxBackground
- `game.py`: Bamboo Forest - Main game entry point and loop. | exports: Game, main
- `levels.py`: Level definitions and construction. | exports: PlatformDef, EnemyDef, LevelDef, LevelState, build_level_state
- `module_auto.py` | exports: SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, GREEN, RED, load_image, Camera
- `save.py`: High score persistence using JSON. | exports: load_high_scores, save_high_score, get_best_score
- `sprites.py`: All sprite classes and procedural pixel-art generators. | exports: generate_panda_frames, generate_bamboo_surface, generate_heal_surface, generate_platform_tile, generate_safe_zone, generate_grass_tuft, generate_mutant_boss, Player
- `ui.py`: Title screen, HUD, transitions, and overlays. | exports: get_font, draw_text, draw_text_shadow, draw_text_left, FloatingText, HUD, TitleScreen, PauseOverlay

## Bamboo_Game/

- `Bamboo_Game/bamboo_app.py` | exports: Panda, Bamboo, MutantPanda, main

## web/

- `web/audio.py`: Procedural sound effect generation via WAV synthesis. | exports: SAMPLE_RATE, AudioManager
- `web/backgrounds.py`: Biome-themed parallax backgrounds. | exports: ForestBackground, VolcanicBackground, BasaltBackground, DesertBackground, CaveBackground, SaltFlatsBackground, MushroomBackground, TidalBackground
- `web/biomes.py`: Biome-specific sprites: mechanics, enemies, NPCs for levels 4-8. | exports: generate_volcanic_tile, generate_basalt_tile, generate_sandstone_tile, generate_limestone_tile, generate_salt_tile, generate_mushroom_tile, generate_tidal_tile, generate_gravity_tile
- `web/config.py`: All game constants, colors, and tuning parameters. | exports: COL_SKY, COL_PANDA_BLACK, COL_PANDA_WHITE, COL_BAMBOO, COL_BAMBOO_JOINT, COL_PLAT_GRASS, COL_PLAT_DIRT, COL_HEAL_PINK
- `web/engine.py`: Camera, particle system, parallax background, and screen shake. | exports: Camera, ScreenShake, Particle, ParticleSystem, ParallaxBackground
- `web/game.py`: Bamboo Forest - Main game entry point and loop (WEB BUILD). | exports: Game, main
- `web/levels.py`: Level definitions and construction. | exports: PlatformDef, EnemyDef, LevelDef, LevelState, build_level_state
- `web/main.py`: Pygbag entry point -- delegates to game.main().
- `web/save.py`: High score persistence using JSON. | exports: load_high_scores, save_high_score, get_best_score
- `web/sprites.py`: All sprite classes and procedural pixel-art generators. | exports: generate_panda_frames, generate_bamboo_surface, generate_heal_surface, generate_platform_tile, generate_safe_zone, generate_grass_tuft, generate_mutant_boss, Player
- `web/ui.py`: Title screen, HUD, transitions, and overlays. | exports: get_font, draw_text, draw_text_shadow, draw_text_left, FloatingText, HUD, TitleScreen, PauseOverlay
