# From: audio.py:70
# Concatenate multiple sample buffers.

def _concat(*buffers: array.array) -> array.array:
    """Concatenate multiple sample buffers."""
    out = array.array("h")
    for b in buffers:
        out.extend(b)
    return out
