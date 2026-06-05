# From: levels.py:91
# Generate bamboo positions attached to STATIC platforms only.

def _scatter_bamboos(platforms: list[PlatformDef], world_width: int,
                     floor_y: int, target_count: int) -> list[tuple[int, int]]:
    """Generate bamboo positions attached to STATIC platforms only.
    Moving platforms are excluded -- bamboo would float when they move.
    """
    positions: list[tuple[int, int]] = []
    # Exclude moving platforms from placement
    static_plats = [p for p in platforms if not p.moving]
    sorted_plats = sorted(static_plats, key=lambda p: p.x)
    if not sorted_plats:
        # Fallback: scatter on floor
        for i in range(target_count):
            bx = 200 + (world_width - 400) * i // max(1, target_count - 1)
            positions.append((bx, floor_y))
        return positions
    for p in sorted_plats:
        margin = min(25, p.w // 4)
        bx = p.x + random.randint(margin, max(margin, p.w - margin))
        positions.append((bx, p.y))
    for p in sorted_plats:
        if p.w >= 220 and len(positions) < target_count:
            bx = p.x + random.randint(10, p.w // 3)
            positions.append((bx, p.y))
    plat_idx = 0
    while len(positions) < target_count:
        p = sorted_plats[plat_idx % len(sorted_plats)]
        bx = p.x + random.randint(0, p.w)
        positions.append((bx, floor_y))
        plat_idx += 1
    return positions
