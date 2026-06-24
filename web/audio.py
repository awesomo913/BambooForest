"""Procedural sound effect generation via WAV synthesis.

WEB BUILD NOTE: `from __future__ import annotations` is critical here.
Pygbag's WASM build may not always expose `pygame.mixer`, so we defer
evaluation of type annotations so the module can import cleanly.
"""

from __future__ import annotations

import array
import math
import random

import pygame

SAMPLE_RATE = 44100


def _sine_samples(freq: float, duration: float, volume: float = 0.5) -> array.array:
    """Generate signed-16-bit sine wave samples."""
    n = int(SAMPLE_RATE * duration)
    buf = array.array("h", [0] * n)
    for i in range(n):
        buf[i] = int(32767 * volume * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))
    return buf


def _square_samples(freq: float, duration: float, volume: float = 0.3) -> array.array:
    """Generate square wave samples."""
    n = int(SAMPLE_RATE * duration)
    period = SAMPLE_RATE / freq if freq > 0 else SAMPLE_RATE
    buf = array.array("h", [0] * n)
    for i in range(n):
        val = 1 if (i % int(period)) < (period / 2) else -1
        buf[i] = int(32767 * volume * val)
    return buf


def _noise_samples(duration: float, volume: float = 0.3) -> array.array:
    """Generate white noise samples."""
    n = int(SAMPLE_RATE * duration)
    amp = int(32767 * volume)
    return array.array("h", [random.randint(-amp, amp) for _ in range(n)])


def _sweep_samples(f_start: float, f_end: float, duration: float,
                   volume: float = 0.5) -> array.array:
    """Generate pitch sweep (linear frequency interpolation)."""
    n = int(SAMPLE_RATE * duration)
    buf = array.array("h", [0] * n)
    phase = 0.0
    for i in range(n):
        t = i / n
        freq = f_start + (f_end - f_start) * t
        phase += 2 * math.pi * freq / SAMPLE_RATE
        buf[i] = int(32767 * volume * math.sin(phase))
    return buf


def _apply_envelope(buf: array.array, attack: float = 0.01,
                    decay: float = 0.0) -> array.array:
    """Apply attack/decay amplitude envelope in-place."""
    n = len(buf)
    attack_n = int(SAMPLE_RATE * attack)
    decay_n = int(SAMPLE_RATE * decay) if decay > 0 else 0
    result = array.array("h", [0] * n)
    for i in range(n):
        env = 1.0
        if i < attack_n and attack_n > 0:
            env = i / attack_n
        if decay_n > 0 and i >= (n - decay_n):
            env *= (n - i) / decay_n
        result[i] = int(buf[i] * env)
    return result


def _concat(*buffers: array.array) -> array.array:
    """Concatenate multiple sample buffers."""
    out = array.array("h")
    for b in buffers:
        out.extend(b)
    return out


def _to_sound(buf: array.array) -> pygame.mixer.Sound:
    """Convert sample buffer to pygame Sound."""
    return pygame.mixer.Sound(buffer=buf)


def _pitch_buf(buf: array.array, pitch: float) -> array.array:
    """Cheap linear resample for pitch shift. pitch>1 = higher/faster."""
    if abs(pitch - 1.0) < 0.015:
        return buf
    n = len(buf)
    new_n = max(4, int(n / pitch))
    out = array.array("h", [0] * new_n)
    for i in range(new_n):
        src = i * pitch
        i0 = int(src)
        if i0 >= n - 1:
            out[i] = buf[-1]
            continue
        f = src - i0
        out[i] = int(buf[i0] * (1 - f) + buf[i0 + 1] * f)
    return out


# Per-sound minimum replay interval (seconds). Prevents rapid stacking.
_MIN_INTERVAL: dict[str, float] = {
    "collect": 0.05,
    "stomp": 0.08,
    "jump": 0.10,
    "hit": 0.15,
    "boss_hit": 0.20,
    "geyser": 0.25,
    "crystal": 0.10,
    "crumble": 0.30,
    "wind": 0.50,
    "ice_slide": 0.20,
    "dash": 0.12,
    "attack": 0.08,
    "slam": 0.12,
    "ice": 0.15,
    "land": 0.10,
    "graft": 0.25,
    "essence": 0.15,
}
_DEFAULT_INTERVAL: float = 0.05

# Global volume for ambient/soft feel
_BASE_VOLUME: float = 0.3


class AudioManager:
    """Generates and caches all game sounds at init."""

    def __init__(self) -> None:
        self.enabled = True
        self.sounds: dict = {}
        self.raw_bufs: dict = {}
        self._last_play_time: dict[str, float] = {}
        self._master_volume = 0.8
        # Web build: mixer may be unavailable. Catch ANY failure and
        # disable audio gracefully instead of crashing the whole game.
        if not hasattr(pygame, "mixer"):
            self.enabled = False
            return
        try:
            pygame.mixer.init(SAMPLE_RATE, -16, 1, 512)
            pygame.mixer.set_num_channels(16)
        except (pygame.error, AttributeError, Exception):
            self.enabled = False
            return

        try:
            self._build_sounds()
        except (pygame.error, AttributeError, Exception):
            self.enabled = False
            self.sounds = {}
            return

    def _build_sounds(self) -> None:
        """Build all procedural sounds. Wrapped so any single failure
        doesn't take down the whole audio system."""
        self.raw_bufs: dict = {}
        def _reg(name: str, buf: array.array) -> None:
            self.raw_bufs[name] = buf
            self.sounds[name] = _to_sound(buf)

        _reg("jump", _apply_envelope(_sweep_samples(200, 600, 0.15, 0.35), 0.005, 0.04))
        _reg("collect", _apply_envelope(
            _concat(
                _sine_samples(800, 0.06, 0.4),
                _sine_samples(1200, 0.1, 0.4),
            ),
            0.005, 0.03,
        ))
        _reg("hit", _apply_envelope(
            _concat(
                _noise_samples(0.08, 0.4),
                _sine_samples(100, 0.12, 0.3),
            ),
            0.005, 0.05,
        ))
        _reg("stomp", _apply_envelope(
            _concat(
                _noise_samples(0.04, 0.35),
                _sine_samples(300, 0.08, 0.35),
            ),
            0.005, 0.03,
        ))
        _reg("menu_select", _apply_envelope(_sine_samples(600, 0.08, 0.3), 0.005, 0.02))
        _reg("boss_hit", _apply_envelope(_square_samples(80, 0.2, 0.35), 0.01, 0.06))
        _reg("victory", _apply_envelope(
            _concat(
                _sine_samples(262, 0.12, 0.35),
                _sine_samples(330, 0.12, 0.35),
                _sine_samples(392, 0.12, 0.35),
                _sine_samples(523, 0.2, 0.35),
            ),
            0.005, 0.06,
        ))
        _reg("death", _apply_envelope(_sweep_samples(400, 80, 0.5, 0.3), 0.01, 0.1))
        # Biome sounds
        _reg("geyser", _apply_envelope(_sweep_samples(100, 400, 0.3, 0.4), 0.02, 0.1))
        _reg("crumble", _apply_envelope(_noise_samples(0.4, 0.3), 0.01, 0.15))
        _reg("wind", _apply_envelope(_noise_samples(0.6, 0.15), 0.1, 0.2))
        _reg("crystal", _apply_envelope(
            _concat(_sine_samples(1000, 0.08, 0.4), _sine_samples(1500, 0.12, 0.3)),
            0.005, 0.04,
        ))
        _reg("ice_slide", _apply_envelope(_sweep_samples(800, 200, 0.2, 0.2), 0.01, 0.08))
        # Cute dance tune
        dance_notes = [523, 659, 784, 1047, 659, 784, 1047, 1319]
        dance_parts = []
        for freq in dance_notes:
            dance_parts.append(_apply_envelope(
                _sine_samples(freq, 0.12, 0.35), 0.005, 0.04))
            dance_parts.append(_sine_samples(1, 0.02, 0.0))
        _reg("dance", _concat(*dance_parts))

        # --- New richer feedback sounds ---
        _reg("dash", _apply_envelope(
            _concat(
                _noise_samples(0.05, 0.28),
                _sweep_samples(280, 920, 0.09, 0.32),
            ),
            0.003, 0.06,
        ))
        _reg("attack", _apply_envelope(
            _concat(
                _square_samples(160, 0.045, 0.38),
                _noise_samples(0.035, 0.32),
            ),
            0.002, 0.025,
        ))
        _reg("slam", _apply_envelope(
            _concat(
                _noise_samples(0.11, 0.42),
                _sine_samples(95, 0.16, 0.38),
            ),
            0.004, 0.09,
        ))
        _reg("ice", _apply_envelope(
            _sweep_samples(1350, 620, 0.16, 0.36),
            0.008, 0.09,
        ))

        # Juicier feedback (graft/essence/land for task)
        _reg("land", _apply_envelope(
            _concat(
                _noise_samples(0.04, 0.25),
                _sine_samples(120, 0.06, 0.22),
            ),
            0.003, 0.04,
        ))
        _reg("graft", _apply_envelope(
            _concat(
                _sine_samples(440, 0.06, 0.35),
                _sine_samples(660, 0.08, 0.32),
                _sine_samples(880, 0.12, 0.28),
            ),
            0.005, 0.05,
        ))
        _reg("essence", _apply_envelope(
            _sweep_samples(900, 1400, 0.12, 0.25),
            0.01, 0.06,
        ))

    def play(self, name: str, pitch: float = 1.0) -> None:
        """Play a sound with 30% volume cap + rate limiting.
        pitch > 1.0 raises pitch (for combo juice etc). Light resample when needed.
        Slight random detune on some sounds for organic feel.
        """
        if not self.enabled or name not in self.sounds:
            return
        now = pygame.time.get_ticks() / 1000.0
        last = self._last_play_time.get(name, -999.0)
        elapsed = now - last
        min_gap = _MIN_INTERVAL.get(name, _DEFAULT_INTERVAL)
        if elapsed < min_gap:
            return

        # Variation: tiny random pitch wobble on lively sounds
        if name in ("jump", "dash", "collect", "attack", "stomp"):
            pitch *= random.uniform(0.96, 1.04)

        use_pitch = abs(pitch - 1.0) > 0.01
        if use_pitch and name in self.raw_bufs:
            pbuf = _pitch_buf(self.raw_bufs[name], pitch)
            snd = _to_sound(pbuf)
            ch = snd.play()
        else:
            ch = self.sounds[name].play()

        if ch:
            master = getattr(self, '_master_volume', 0.8)
            vol = master * _BASE_VOLUME * (0.7 if elapsed < 0.2 else 1.0)
            ch.set_volume(vol)
        self._last_play_time[name] = now

    def toggle(self) -> None:
        """Toggle sound on/off."""
        self.enabled = not self.enabled

    def set_master_volume(self, vol: float) -> None:
        """Set master volume 0.0-1.0. Affects future plays."""
        self._master_volume = max(0.0, min(1.0, float(vol)))
