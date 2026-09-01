# Assets

This directory is **optional**. The game draws every sprite at runtime with
pygame primitives when a file is missing, so it is playable with this directory
empty. Drop a real file in at the matching name and it takes priority
automatically — no code change needed.

## Images

| File | Drawn at | Placeholder |
|---|---|---|
| `spaceship.png` | 48×48 | cyan/blue arrowhead |
| `bullet.png` | 6×16 | yellow capsule |
| `enemy.png` | 40×40 | red downward triangle |
| `enemy_fast.png` | 40×40 | orange downward triangle |
| `boss.png` | 140×90 | purple ellipse |
| `powerup.png` | 26×26 | green orb |
| `background.png` | 800×600 | dark starfield |
| `explosion_0.png` … `explosion_4.png` | 64×64 | expanding blast, 5 frames |

Images are scaled to the size above, so source art need not match exactly.
Sizes live in `settings.py`.

## Sounds

| File | Used for |
|---|---|
| `background_music.mp3` | looping music |
| `shoot.wav` | firing |
| `explosion.wav` | a kill or a hit |
| `powerup.wav` | collecting a power-up |

Missing sounds — and a machine with no audio device at all — degrade to silence
rather than crashing, so the game runs headless and in CI.
