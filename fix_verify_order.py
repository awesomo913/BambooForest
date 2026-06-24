import re
with open('tests/verify.py', 'r', encoding='utf-8') as f:
    txt = f.read()

m = re.search(r'(?s)^def verify_jump_buffer\(\) -> None:.*?(?=\n(?=def |SCENARIOS|if __name__|class |$))', txt, re.M)
if not m:
    m = re.search(r'(?s)def verify_jump_buffer\(\) -> None:.*', txt)
if m:
    func = m.group(0).rstrip() + '\n\n'
    txt2 = txt.replace(m.group(0), '', 1)
    # insert after run_scenario
    anchor = 'def run_scenario(name: str, func) -> None:\n    """Wrapper that prints PASS/FAIL for a verification scenario."""\n    try:\n        func()\n        print(f"[PASS] {name}")\n    except AssertionError as e:\n        print(f"[FAIL] {name}: {e}")\n    except Exception as e:\n        print(f"[ERROR] {name}: {type(e).__name__}: {e}")\n\n'
    if anchor in txt2:
        txt2 = txt2.replace(anchor, anchor + func, 1)
    else:
        txt2 = re.sub(r'(?m)^(def verify_dash)', func + r'\1', txt2, count=1)
    with open('tests/verify.py', 'w', encoding='utf-8') as f:
        f.write(txt2)
    print('moved jump_buffer def before SCENARIOS')
print('jump defs count:', open('tests/verify.py', encoding='utf-8').read().count('def verify_jump_buffer'))
