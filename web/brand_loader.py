"""Post-build: brand the pygbag loading screen to the Revolutionary Designs
"Game World" theme (cream/sage/terra) instead of pygbag's default
powderblue page + green/blue "please wait" box.

Run AFTER `pygbag --build main.py`:

    python brand_loader.py            # patches build/web/index.html in place

Idempotent. The override CSS is appended inside the existing <style> block so
it wins the cascade. Loader layers (#transfer z=3, #infobox z=4) sit BELOW the
game canvas (z=5), so they're covered the moment the game starts — they can
never linger over gameplay.
"""
from pathlib import Path

INDEX = Path(__file__).parent / "build" / "web" / "index.html"

MARKER = "/* === RevDesigns Game World loader === */"

OVERRIDE = MARKER + """
html,body{height:100%}
body{background:#f3ead8 !important;font-family:'Work Sans',system-ui,-apple-system,sans-serif !important;color:#2c2416}
#transfer{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;z-index:3}
#transfer::before{content:'Bamboo Forest';font-weight:700;font-size:24px;color:#365239;letter-spacing:.01em}
#status{display:block !important;margin:0 !important;color:#5f5440 !important;font-weight:600;font-size:14px}
#progress{height:14px !important;width:260px !important;accent-color:#6b8f6b}
#infobox{position:fixed !important;left:50% !important;right:auto !important;top:auto !important;bottom:46px !important;transform:translateX(-50%);background:#fbf6ea !important;color:#5f5440 !important;border:2px solid #d6c8ac !important;border-radius:8px !important;box-shadow:0 4px 0 rgba(120,90,58,.14);padding:8px 16px !important;font-weight:600 !important;z-index:4}
"""


def main() -> None:
    if not INDEX.exists():
        raise SystemExit(f"build output not found: {INDEX} (run pygbag --build first)")
    html = INDEX.read_text(encoding="utf-8")
    if MARKER in html:
        print("already branded — no change")
        return
    if "</style>" not in html:
        raise SystemExit("no </style> in build index.html — pygbag template changed?")
    html = html.replace("</style>", OVERRIDE + "</style>", 1)
    INDEX.write_text(html, encoding="utf-8")
    print(f"branded loader -> {INDEX}")


if __name__ == "__main__":
    main()
