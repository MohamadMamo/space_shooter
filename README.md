# space_shooter

A space shooter built with Python and Pygame. Fly a ship, clear waves of
enemies, build combo multipliers to upgrade your weapon, and fight a boss every
fifth level.

**No art files required.** Every sprite has a runtime-drawn fallback, so the game
is playable straight after `pip install`. Drop real PNGs into `assets/` and they
take over automatically — see [`assets/README.md`](assets/README.md).

## Features

- Eight-direction movement with the arrow keys, fire with space.
- Three weapon tiers, earned by chaining kills without letting an enemy through.
- Power-ups that grant temporary rapid fire.
- A boss every 5 levels, with a health bar; faster enemies every 3.
- Combo multiplier, health bar, and a persistent high score.
- Animated explosions, pause, and a game-over screen with restart.
- Frame-rate independent movement — the game plays the same at 30 or 144 FPS.

## Controls

| Key | Action |
|---|---|
| ← → ↑ ↓ | Move |
| Space | Fire (held; rate-limited) |
| P | Pause / resume |
| R | Restart, on the game-over screen |
| Esc | Quit |

## Installation

```bash
git clone https://github.com/MohamadMamo/space_shooter.git
cd space_shooter
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

Paths are anchored to the source directory, so this works from any working
directory.

## Tests

```bash
pip install -r requirements-dev.txt
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest
```

The suite runs headless — no window or audio device needed — and covers the
asset fallback, the restart path, the fire-rate cap, damage handling,
frame-rate independence, and high-score persistence.

## Layout

| File | Role |
|---|---|
| `main.py` | Loop, input, collision resolution, rendering |
| `game_state.py` | All mutable run state, with a single `reset()` |
| `entity.py` | Shared position/draw base for every sprite |
| `spaceship.py` | Player ship: health, weapon tier, power-ups |
| `enemy.py` | `Enemy` and `Boss` |
| `bullet.py`, `powerup.py`, `explosion.py` | Remaining entities |
| `utils.py` | Asset loading with placeholder art, audio, high score |
| `settings.py` | All tunable constants |

Nothing runs at import time: `pygame.init()`, the window, and asset loading all
happen inside `init_game()`, which is what lets the tests import these modules.

## Tuning

Gameplay constants live in `settings.py` — speeds (pixels per second), damage,
scoring, cooldowns, and wave sizes.

## License

MIT — see [LICENSE](LICENSE).
