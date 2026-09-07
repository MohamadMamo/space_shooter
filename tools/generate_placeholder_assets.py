#!/usr/bin/env python3
"""
Generate placeholder game assets.

*** These are PLACEHOLDER assets, not final art/audio. ***
They exist so the game can be cloned and run out of the box. Replace the
PNGs and WAVs under assets/ with real artwork and sound effects whenever
they're ready -- nothing else in the codebase needs to change to swap
them, since settings.py just points at these filenames.

Usage:
    python tools/generate_placeholder_assets.py

Regenerates every file settings.py declares under assets/: 12 PNGs (5
single-image assets, 5 explosion animation frames, the powerup and the
background -- all drawn with pygame primitives) and 4 silent WAV files.
"""

import os
import struct
import sys

import pygame

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import settings  # noqa: E402


def _ensure_assets_dir():
    assets_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"
    )
    os.makedirs(assets_dir, exist_ok=True)
    return assets_dir


def _save(surface, path):
    pygame.image.save(surface, path)
    print(f"wrote {path}")


def make_spaceship(path):
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (60, 200, 255), [(20, 0), (0, 40), (20, 30), (40, 40)])
    _save(surf, path)


def make_bullet(path):
    surf = pygame.Surface((6, 14), pygame.SRCALPHA)
    pygame.draw.rect(surf, (255, 240, 80), (0, 0, 6, 14), border_radius=2)
    _save(surf, path)


def make_enemy(path):
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (220, 60, 60), [(0, 0), (30, 0), (15, 30)])
    _save(surf, path)


def make_enemy_fast(path):
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (255, 140, 0), [(0, 0), (30, 0), (15, 30)])
    _save(surf, path)


def make_boss(path):
    surf = pygame.Surface((120, 80), pygame.SRCALPHA)
    pygame.draw.rect(surf, (150, 30, 150), (0, 0, 120, 80), border_radius=12)
    pygame.draw.circle(surf, (255, 255, 255), (60, 40), 15)
    _save(surf, path)


def make_explosion_frame(path, radius):
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 165, 0), (20, 20), radius)
    pygame.draw.circle(surf, (255, 255, 0), (20, 20), max(radius - 6, 1))
    _save(surf, path)


def make_powerup(path):
    surf = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(surf, (60, 255, 120), (10, 10), 10)
    _save(surf, path)


def make_background(path):
    surf = pygame.Surface((settings.WIDTH, settings.HEIGHT))
    surf.fill((5, 5, 20))
    _save(surf, path)


def _write_silent_wav(path, duration_seconds=1.0, sample_rate=44100):
    """Write a minimal silent, mono, 16-bit PCM WAV file."""
    num_samples = int(duration_seconds * sample_rate)
    data = b"\x00\x00" * num_samples
    byte_rate = sample_rate * 2
    with open(path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + len(data)))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, byte_rate, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", len(data)))
        f.write(data)
    print(f"wrote {path}")


def main():
    _ensure_assets_dir()
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.HIDDEN)

    make_spaceship(settings.SPACESHIP_IMAGE)
    make_bullet(settings.BULLET_IMAGE)
    make_enemy(settings.ENEMY_IMAGE)
    make_enemy_fast(settings.ENEMY_FAST_IMAGE)
    make_boss(settings.BOSS_IMAGE)
    radii = [6, 10, 14, 18, 20]
    for frame_path, radius in zip(settings.EXPLOSION_FRAMES, radii):
        make_explosion_frame(frame_path, radius)
    make_powerup(settings.POWERUP_IMAGE)
    make_background(settings.BACKGROUND_IMAGE)

    for wav_path in (
        settings.BACKGROUND_MUSIC,
        settings.SHOOT_SOUND,
        settings.EXPLOSION_SOUND,
        settings.POWERUP_SOUND,
    ):
        _write_silent_wav(wav_path, duration_seconds=0.2)

    pygame.quit()
    print("Done. Replace these placeholders with real art/audio when ready.")


if __name__ == "__main__":
    main()
