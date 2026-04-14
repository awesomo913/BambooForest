"""Procedural sound effect generation via WAV synthesis."""

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


class AudioManager:
    """Generates and caches all game sounds at init."""

    def __init__(self) -> None:
        self.enabled = True
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            pygame.mixer.init(SAMPLE_RATE, -16, 1, 512)
        except pygame.error:
            self.enabled = False
            return

        self.sounds["jump"] = _to_sound(
            _apply_envelope(_sweep_samples(200, 600, 0.15, 0.35), 0.005, 0.04)
        )
        self.sounds["collect"] = _to_sound(
            _apply_envelope(
                _concat(
                    _sine_samples(800, 0.06, 0.4),
                    _sine_samples(1200, 0.1, 0.4),
                ),
                0.005, 0.03,
            )
        )
        self.sounds["hit"] = _to_sound(
            _apply_envelope(
                _concat(
                    _noise_samples(0.08, 0.4),
                    _sine_samples(100, 0.12, 0.3),
                ),
                0.005, 0.05,
            )
        )
        self.sounds["stomp"] = _to_sound(
            _apply_envelope(
                _concat(
                    _noise_samples(0.04, 0.35),
                    _sine_samples(300, 0.08, 0.35),
                ),
                0.005, 0.03,
            )
        )
        self.sounds["menu_select"] = _to_sound(
            _apply_envelope(_sine_samples(600, 0.08, 0.3), 0.005, 0.02)
        )
        self.sounds["boss_hit"] = _to_sound(
            _apply_envelope(_square_samples(80, 0.2, 0.35), 0.01, 0.06)
        )
        self.sounds["victory"] = _to_sound(
            _apply_envelope(
                _concat(
                    _sine_samples(262, 0.12, 0.35),
                    _sine_samples(330, 0.12, 0.35),
                    _sine_samples(392, 0.12, 0.35),
                    _sine_samples(523, 0.2, 0.35),
                ),
                0.005, 0.06,
            )
        )
        self.sounds["death"] = _to_sound(
            _apply_envelope(_sweep_samples(400, 80, 0.5, 0.3), 0.01, 0.1)
        )
        # Biome sounds
        self.sounds["geyser"] = _to_sound(
            _apply_envelope(_sweep_samples(100, 400, 0.3, 0.4), 0.02, 0.1)
        )
        self.sounds["crumble"] = _to_sound(
            _apply_envelope(_noise_samples(0.4, 0.3), 0.01, 0.15)
        )
        self.sounds["wind"] = _to_sound(
            _apply_envelope(_noise_samples(0.6, 0.15), 0.1, 0.2)
        )
        self.sounds["crystal"] = _to_sound(
            _apply_envelope(
                _concat(_sine_samples(1000, 0.08, 0.4), _sine_samples(1500, 0.12, 0.3)),
                0.005, 0.04,
            )
        )
        self.sounds["ice_slide"] = _to_sound(
            _apply_envelope(_sweep_samples(800, 200, 0.2, 0.2), 0.01, 0.08)
        )

    def play(self, name: str) -> None:
        """Play a named sound if enabled."""
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def toggle(self) -> None:
        """Toggle sound on/off."""
        self.enabled = not self.enabled
