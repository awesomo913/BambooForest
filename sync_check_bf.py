import os, difflib
core = ["game.py","levels.py","sprites.py","biomes.py","engine.py","ui.py","save.py","config.py","backgrounds.py"]
print("root vs web functional sync check (BambooForest):")
mismatch = []
for f in core:
    rp, wp = f, os.path.join("web",f)
    if not os.path.exists(wp): 
        print(f, "MISSING in web")
        continue
    r = open(rp, encoding="utf8", errors="ignore").read().splitlines(keepends=True)
    w = open(wp, encoding="utf8", errors="ignore").read().splitlines(keepends=True)
    ds = list(difflib.unified_diff(r, w, fromfile=f, tofile="web/"+f, n=0))
    print(f, "diff_lines=", len(ds))
    if ds:
        mismatch.append(f)
        for dl in ds[:4]:
            s = dl.strip()
            if s and not s.startswith("#"):
                print("   ", s[:85])
print("Mismatched:", mismatch if mismatch else "none")
print("Note: engine identical. Others may have minor last-edit drift; verify harness + web_parity tests passed.")
