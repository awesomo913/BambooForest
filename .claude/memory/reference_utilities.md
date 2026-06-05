---
name: BambooForest Utilities
description: Reusable functions and their locations in BambooForest
type: reference
---

# Reusable Functions in BambooForest

| Function | Module | Purpose |
|----------|--------|---------|
| `SAMPLE_RATE` | `audio.py` | -- |
| `AudioManager` | `audio.py` | Generates and caches all game sounds at init. |
| `ForestBackground` | `backgrounds.py` | Original bamboo forest -- blue sky, green mountains, pine trees. |
| `VolcanicBackground` | `backgrounds.py` | Red-orange sky, dark volcanic peaks, lava glow, ash particles. |
| `BasaltBackground` | `backgrounds.py` | Misty gray sky, hexagonal column silhouettes, sea spray. |
| `DesertBackground` | `backgrounds.py` | Warm orange sky, sand dunes, distant mesas, heat haze. |
| `CaveBackground` | `backgrounds.py` | Dark cave with stalactites + stalagmites + glowworm specks. |
| `SaltFlatsBackground` | `backgrounds.py` | Pale sky, snowy Andes silhouettes, mirror-flat salt surface. |
| `MushroomBackground` | `backgrounds.py` | Bioluminescent underground mushroom forest. |
| `TidalBackground` | `backgrounds.py` | Stormy coastal ruin with rocks, lighthouse, and waves. |
| `GravityBackground` | `backgrounds.py` | Arcane void with floating structures and pulsing veins. |
| `CorruptedForestBackground` | `backgrounds.py` | Sickly forest with purple-tinted vegetation -- corruption creeping in. |
| `Panda` | `bamboo_app.py` | -- |
| `Bamboo` | `bamboo_app.py` | -- |
| `MutantPanda` | `bamboo_app.py` | -- |
| `main` | `bamboo_app.py` | -- |
| `BASE_DIR` | `bamboo_forest.py` | -- |
| `load_sprite` | `bamboo_forest.py` | Loads an image if it exists, otherwise returns a colored block. |
| `Panda` | `bamboo_forest.py` | -- |
| `Platform` | `bamboo_forest.py` | -- |
| `Bamboo` | `bamboo_forest.py` | -- |
| `HealingItem` | `bamboo_forest.py` | -- |
| `MutantPanda` | `bamboo_forest.py` | -- |
| `Camera` | `bamboo_forest.py` | -- |
| `build_level` | `bamboo_forest.py` | -- |
| `draw_text` | `bamboo_forest.py` | -- |
| `generate_volcanic_tile` | `biomes.py` | Dark volcanic basalt with orange lava crack highlights. |
| `generate_basalt_tile` | `biomes.py` | Hexagonal basalt columns -- dark gray with top lip. |
| `generate_sandstone_tile` | `biomes.py` | Layered tan sandstone with erosion marks. |
| `generate_limestone_tile` | `biomes.py` | Pale gray-tan limestone cave floor with fossil marks. |
| `generate_salt_tile` | `biomes.py` | Pale blue-white salt crystal surface, reflective. |
| `generate_mushroom_tile` | `biomes.py` | Bioluminescent fungal soil -- dark purple with glowing spores. |
| `generate_tidal_tile` | `biomes.py` | Barnacled coastal stone with teal water stains. |
| `generate_gravity_tile` | `biomes.py` | Arcane metal with glowing circuit veins. |
| `generate_corrupted_tile` | `biomes.py` | Sickly forest ground -- dark green with purple corruption veins. |
| `generate_lair_tile` | `biomes.py` | Corrupted boss-lair ground -- crimson shadow with dark veins. |
| `COL_SKY` | `config.py` | -- |
| `COL_PANDA_BLACK` | `config.py` | -- |
| `COL_PANDA_WHITE` | `config.py` | -- |
| `COL_BAMBOO` | `config.py` | -- |
| `COL_BAMBOO_JOINT` | `config.py` | -- |
| `COL_PLAT_GRASS` | `config.py` | -- |
| `COL_PLAT_DIRT` | `config.py` | -- |
| `COL_HEAL_PINK` | `config.py` | -- |
| `COL_HEAL_RED` | `config.py` | -- |
| `COL_GOLD` | `config.py` | -- |
| `Camera` | `engine.py` | Smooth-follow camera. Logic state is float, render state is int. |
| `ScreenShake` | `engine.py` | -- |
| `Particle` | `engine.py` | -- |
| `ParticleSystem` | `engine.py` | -- |
| `ParallaxBackground` | `engine.py` | Clean parallax with seamlessly-tileable layers. |
| `Game` | `game.py` | Main game class -- owns the loop and state machine. |
| `main` | `game.py` | -- |
| `PlatformDef` | `levels.py` | -- |
| `EnemyDef` | `levels.py` | -- |
| `LevelDef` | `levels.py` | -- |
| `LevelState` | `levels.py` | Instantiated level with all sprite groups. |
| `build_level_state` | `levels.py` | -- |
| `SCREEN_WIDTH` | `module_auto.py` | -- |
| `SCREEN_HEIGHT` | `module_auto.py` | -- |
| `FPS` | `module_auto.py` | -- |
| `WHITE` | `module_auto.py` | -- |
| `GREEN` | `module_auto.py` | -- |
| `RED` | `module_auto.py` | -- |
| `load_image` | `module_auto.py` | -- |
| `Camera` | `module_auto.py` | -- |
| `Panda` | `module_auto.py` | -- |
| `Platform` | `module_auto.py` | -- |
| `load_high_scores` | `save.py` | Load high scores from disk. Returns sorted list of {score, level}. |
| `save_high_score` | `save.py` | Add score if it qualifies for top 5. Returns True if it made the list. |
| `get_best_score` | `save.py` | Return the highest saved score, or 0. |
| `generate_panda_frames` | `sprites.py` | Cleaner panda with rounder proportions and visible detail. |
| `generate_bamboo_surface` | `sprites.py` | 20x55 bamboo stalk with joints and leaves. |
| `generate_heal_surface` | `sprites.py` | 25x25 heart shape. |
| `generate_platform_tile` | `sprites.py` | Asian-themed platform: polished wood grain + bamboo cross-sections. |
| `generate_safe_zone` | `sprites.py` | Asian temple grove: torii gate, pagoda silhouette, cherry blossoms. |
| `generate_grass_tuft` | `sprites.py` | Small decorative grass blades. |
| `generate_mutant_boss` | `sprites.py` | Procedural mutant panda boss -- corrupted, larger, menacing. |
| `Player` | `sprites.py` | The panda protagonist with full physics and animation. |
| `Platform` | `sprites.py` | -- |
| `MovingPlatform` | `sprites.py` | -- |
| `get_font` | `ui.py` | -- |
| `draw_text` | `ui.py` | -- |
| `draw_text_shadow` | `ui.py` | -- |
| `draw_text_left` | `ui.py` | -- |
| `FloatingText` | `ui.py` | -- |
| `HUD` | `ui.py` | -- |
| `TitleScreen` | `ui.py` | -- |
| `PauseOverlay` | `ui.py` | Pause screen with compact enemy encyclopedia (read while waiting). |
| `GameOverScreen` | `ui.py` | -- |
| `VictoryScreen` | `ui.py` | -- |
| `Panda` | `Bamboo_Game/bamboo_app.py` | -- |
| `Bamboo` | `Bamboo_Game/bamboo_app.py` | -- |
| `MutantPanda` | `Bamboo_Game/bamboo_app.py` | -- |
| `main` | `Bamboo_Game/bamboo_app.py` | -- |
| `SAMPLE_RATE` | `web/audio.py` | -- |
| `AudioManager` | `web/audio.py` | Generates and caches all game sounds at init. |
| `ForestBackground` | `web/backgrounds.py` | Original bamboo forest -- blue sky, green mountains, pine trees. |
| `VolcanicBackground` | `web/backgrounds.py` | Red-orange sky, dark volcanic peaks, lava glow, ash particles. |
| `BasaltBackground` | `web/backgrounds.py` | Misty gray sky, hexagonal column silhouettes, sea spray. |
| `DesertBackground` | `web/backgrounds.py` | Warm orange sky, sand dunes, distant mesas, heat haze. |
| `CaveBackground` | `web/backgrounds.py` | Dark cave with stalactites + stalagmites + glowworm specks. |
| `SaltFlatsBackground` | `web/backgrounds.py` | Pale sky, snowy Andes silhouettes, mirror-flat salt surface. |
| `MushroomBackground` | `web/backgrounds.py` | Bioluminescent underground mushroom forest. |
| `TidalBackground` | `web/backgrounds.py` | Stormy coastal ruin with rocks, lighthouse, and waves. |
| `GravityBackground` | `web/backgrounds.py` | Arcane void with floating structures and pulsing veins. |
| `CorruptedForestBackground` | `web/backgrounds.py` | Sickly forest with purple-tinted vegetation -- corruption creeping in. |
| `generate_volcanic_tile` | `web/biomes.py` | Dark volcanic basalt with orange lava crack highlights. |
| `generate_basalt_tile` | `web/biomes.py` | Hexagonal basalt columns -- dark gray with top lip. |
| `generate_sandstone_tile` | `web/biomes.py` | Layered tan sandstone with erosion marks. |
| `generate_limestone_tile` | `web/biomes.py` | Pale gray-tan limestone cave floor with fossil marks. |
| `generate_salt_tile` | `web/biomes.py` | Pale blue-white salt crystal surface, reflective. |
| `generate_mushroom_tile` | `web/biomes.py` | Bioluminescent fungal soil -- dark purple with glowing spores. |
| `generate_tidal_tile` | `web/biomes.py` | Barnacled coastal stone with teal water stains. |
| `generate_gravity_tile` | `web/biomes.py` | Arcane metal with glowing circuit veins. |
| `generate_corrupted_tile` | `web/biomes.py` | Sickly forest ground -- dark green with purple corruption veins. |
| `generate_lair_tile` | `web/biomes.py` | Corrupted boss-lair ground -- crimson shadow with dark veins. |
| `COL_SKY` | `web/config.py` | -- |
| `COL_PANDA_BLACK` | `web/config.py` | -- |
| `COL_PANDA_WHITE` | `web/config.py` | -- |
| `COL_BAMBOO` | `web/config.py` | -- |
| `COL_BAMBOO_JOINT` | `web/config.py` | -- |
| `COL_PLAT_GRASS` | `web/config.py` | -- |
| `COL_PLAT_DIRT` | `web/config.py` | -- |
| `COL_HEAL_PINK` | `web/config.py` | -- |
| `COL_HEAL_RED` | `web/config.py` | -- |
| `COL_GOLD` | `web/config.py` | -- |
| `Camera` | `web/engine.py` | Smooth-follow camera. Logic state is float, render state is int. |
| `ScreenShake` | `web/engine.py` | -- |
| `Particle` | `web/engine.py` | -- |
| `ParticleSystem` | `web/engine.py` | -- |
| `ParallaxBackground` | `web/engine.py` | Clean parallax with seamlessly-tileable layers. |
| `Game` | `web/game.py` | Main game class -- owns the loop and state machine. |
| `main` | `web/game.py` | Async entry point for Pygbag/WASM. |
| `PlatformDef` | `web/levels.py` | -- |
| `EnemyDef` | `web/levels.py` | -- |
| `LevelDef` | `web/levels.py` | -- |
| `LevelState` | `web/levels.py` | Instantiated level with all sprite groups. |
| `build_level_state` | `web/levels.py` | -- |
| `load_high_scores` | `web/save.py` | Load high scores from disk. Returns sorted list of {score, level}. |
| `save_high_score` | `web/save.py` | Add score if it qualifies for top 5. Returns True if it made the list. |
| `get_best_score` | `web/save.py` | Return the highest saved score, or 0. |
| `generate_panda_frames` | `web/sprites.py` | Cleaner panda with rounder proportions and visible detail. |
| `generate_bamboo_surface` | `web/sprites.py` | 20x55 bamboo stalk with joints and leaves. |
| `generate_heal_surface` | `web/sprites.py` | 25x25 heart shape. |
| `generate_platform_tile` | `web/sprites.py` | Asian-themed platform: polished wood grain + bamboo cross-sections. |
| `generate_safe_zone` | `web/sprites.py` | Asian temple grove: torii gate, pagoda silhouette, cherry blossoms. |
| `generate_grass_tuft` | `web/sprites.py` | Small decorative grass blades. |
| `generate_mutant_boss` | `web/sprites.py` | Procedural mutant panda boss -- corrupted, larger, menacing. |
| `Player` | `web/sprites.py` | The panda protagonist with full physics and animation. |
| `Platform` | `web/sprites.py` | -- |
| `MovingPlatform` | `web/sprites.py` | -- |
| `get_font` | `web/ui.py` | -- |
| `draw_text` | `web/ui.py` | -- |
| `draw_text_shadow` | `web/ui.py` | -- |
| `draw_text_left` | `web/ui.py` | -- |
| `FloatingText` | `web/ui.py` | -- |
| `HUD` | `web/ui.py` | -- |
| `TitleScreen` | `web/ui.py` | -- |
| `PauseOverlay` | `web/ui.py` | Pause screen with compact enemy encyclopedia (read while waiting). |
| `GameOverScreen` | `web/ui.py` | -- |
| `VictoryScreen` | `web/ui.py` | -- |
