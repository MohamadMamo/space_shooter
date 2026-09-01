# utils.py

import os
import tempfile

import pygame

from settings import (
    ASSETS_DIR, BACKGROUND_IMAGE, BACKGROUND_MUSIC, BLUE, BOSS_IMAGE, BOSS_SIZE,
    BULLET_IMAGE, BULLET_SIZE, CYAN, DARK, ENEMY_FAST_IMAGE, ENEMY_IMAGE,
    ENEMY_SIZE, EXPLOSION_FRAMES, EXPLOSION_SIZE, EXPLOSION_SOUND, HEIGHT,
    HIGHSCORE_FILE, ORANGE, POWERUP_IMAGE, POWERUP_SIZE, POWERUP_SOUND, PURPLE,
    RED, SHOOT_SOUND, SPACESHIP_IMAGE, SPACESHIP_SIZE, WHITE, WIDTH, YELLOW,
)


# --------------------------------------------------------------------------
# Placeholder art
#
# The repository ships without binary assets, so every sprite has a drawing
# function that renders it with pygame primitives. A real PNG at the expected
# path always wins; the placeholder is only used when the file is absent.
# --------------------------------------------------------------------------

GREEN_GLOW = (80, 230, 120)


def _surface(size):
    return pygame.Surface(size, pygame.SRCALPHA)


def draw_ship(size):
    surf = _surface(size)
    w, h = size
    pygame.draw.polygon(surf, CYAN, [(w // 2, 0), (w, h - 6), (w // 2, h - 14), (0, h - 6)])
    pygame.draw.polygon(surf, BLUE, [(w // 2, 6), (w - 8, h - 10), (8, h - 10)])
    pygame.draw.rect(surf, WHITE, (w // 2 - 3, h - 16, 6, 10))
    return surf


def draw_enemy(size, color=RED):
    surf = _surface(size)
    w, h = size
    pygame.draw.polygon(surf, color, [(0, 0), (w, 0), (w // 2, h)])
    pygame.draw.circle(surf, WHITE, (w // 2, h // 3), max(2, w // 10))
    return surf


def draw_enemy_fast(size):
    return draw_enemy(size, color=ORANGE)


def draw_boss(size):
    surf = _surface(size)
    w, h = size
    pygame.draw.ellipse(surf, PURPLE, (0, 0, w, h))
    pygame.draw.ellipse(surf, DARK, (w // 4, h // 4, w // 2, h // 3))
    for i in range(3):
        x = w // 4 + i * (w // 4)
        pygame.draw.circle(surf, YELLOW, (x, int(h * 0.75)), max(3, w // 30))
    return surf


def draw_bullet(size):
    surf = _surface(size)
    w, h = size
    pygame.draw.rect(surf, YELLOW, (0, 0, w, h), border_radius=max(1, w // 2))
    return surf


def draw_powerup(size):
    surf = _surface(size)
    w, h = size
    pygame.draw.circle(surf, GREEN_GLOW, (w // 2, h // 2), w // 2)
    pygame.draw.circle(surf, WHITE, (w // 2, h // 2), max(2, w // 4))
    return surf


def draw_background(size):
    """A dark starfield. Deterministic so it looks the same every launch."""
    surf = pygame.Surface(size)
    surf.fill(DARK)
    w, h = size
    seed = 12345
    for _ in range(160):
        # Small LCG keeps this dependency-free and reproducible.
        seed = (seed * 1103515245 + 12345) % (2 ** 31)
        x = seed % w
        seed = (seed * 1103515245 + 12345) % (2 ** 31)
        y = seed % h
        shade = 90 + (seed % 140)
        pygame.draw.circle(surf, (shade, shade, shade), (x, y), 1)
    return surf


def draw_explosion_frame(size, index, total):
    """One frame of an expanding, fading blast."""
    surf = _surface(size)
    w, h = size
    progress = (index + 1) / total
    radius = int(w / 2 * progress)
    alpha = max(0, int(255 * (1 - progress)))
    for ring_color, scale in ((WHITE, 0.4), (YELLOW, 0.7), (ORANGE, 1.0)):
        ring = int(radius * scale)
        if ring > 0:
            layer = _surface(size)
            pygame.draw.circle(layer, (*ring_color, alpha), (w // 2, h // 2), ring)
            surf.blit(layer, (0, 0))
    return surf


def _convert(surface):
    """Convert to the display format when a display exists (big blit speedup)."""
    if pygame.display.get_surface() is None:
        return surface
    return surface.convert_alpha() if surface.get_flags() & pygame.SRCALPHA else surface.convert()


def load_image(path, size, drawer):
    """Load `path` scaled to `size`, or draw a placeholder if it is missing.

    Call only after pygame.display.set_mode(), so surfaces can be converted.
    """
    try:
        if os.path.exists(path):
            image = pygame.image.load(str(path))
            return _convert(pygame.transform.smoothscale(image, size))
    except pygame.error as exc:
        print(f"[assets] could not load {path} ({exc}); using placeholder art")
    return _convert(drawer(size))


def load_assets():
    """Build the asset dict, falling back to generated art for missing files."""
    explosion_total = len(EXPLOSION_FRAMES)
    explosion = []
    for i, frame_path in enumerate(EXPLOSION_FRAMES):
        explosion.append(
            load_image(
                frame_path,
                EXPLOSION_SIZE,
                lambda size, i=i: draw_explosion_frame(size, i, explosion_total),
            )
        )

    return {
        "spaceship": load_image(SPACESHIP_IMAGE, SPACESHIP_SIZE, draw_ship),
        "bullet": load_image(BULLET_IMAGE, BULLET_SIZE, draw_bullet),
        "enemy": load_image(ENEMY_IMAGE, ENEMY_SIZE, draw_enemy),
        "enemy_fast": load_image(ENEMY_FAST_IMAGE, ENEMY_SIZE, draw_enemy_fast),
        "boss": load_image(BOSS_IMAGE, BOSS_SIZE, draw_boss),
        "explosion": explosion,
        "powerup": load_image(POWERUP_IMAGE, POWERUP_SIZE, draw_powerup),
        "background": load_image(BACKGROUND_IMAGE, (WIDTH, HEIGHT), draw_background),
    }


# --------------------------------------------------------------------------
# Sound
# --------------------------------------------------------------------------

class NullSound:
    """Stands in for a Sound when the mixer or the file is unavailable.

    Lets the game run headless (and in CI) without guarding every play() call.
    """

    def play(self, *args, **kwargs):
        return None

    def stop(self, *args, **kwargs):
        return None

    def set_volume(self, *args, **kwargs):
        return None


def mixer_available():
    return pygame.mixer.get_init() is not None


def init_mixer():
    """Initialise the mixer, tolerating machines with no audio device."""
    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        return True
    except pygame.error as exc:
        print(f"[audio] mixer unavailable ({exc}); running silent")
        return False


def _load_sound(path):
    if not mixer_available() or not os.path.exists(path):
        return NullSound()
    try:
        return pygame.mixer.Sound(str(path))
    except pygame.error as exc:
        print(f"[audio] could not load {path} ({exc})")
        return NullSound()


def load_sounds():
    """Load the effect sounds. Never raises, and never starts playback."""
    return {
        "shoot": _load_sound(SHOOT_SOUND),
        "explosion": _load_sound(EXPLOSION_SOUND),
        "powerup": _load_sound(POWERUP_SOUND),
    }


def start_music():
    """Start looping background music if both the mixer and the file exist."""
    if not mixer_available() or not os.path.exists(BACKGROUND_MUSIC):
        return False
    try:
        pygame.mixer.music.load(str(BACKGROUND_MUSIC))
        pygame.mixer.music.play(-1)
        return True
    except pygame.error as exc:
        print(f"[audio] could not play background music ({exc})")
        return False


# --------------------------------------------------------------------------
# High score
# --------------------------------------------------------------------------

def load_highscore():
    """Read the stored high score, treating a missing or corrupt file as 0."""
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def save_highscore(score):
    """Write the high score atomically so a crash cannot corrupt the file."""
    directory = os.path.dirname(HIGHSCORE_FILE) or "."
    try:
        fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".highscore-")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(str(int(score)))
            os.replace(tmp_path, HIGHSCORE_FILE)
        except BaseException:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise
        return True
    except OSError as exc:
        print(f"[highscore] could not save ({exc})")
        return False
