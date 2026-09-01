# main.py

import random

import pygame

from game_state import GameState
from settings import (
    BOSS_BULLET_DAMAGE, BOSS_CONTACT_DAMAGE, BOSS_SCORE, COMBO_UPGRADE_STEP,
    ENEMY_CONTACT_DAMAGE, ENEMY_SCORE, FPS, HEIGHT, POWERUP_SPAWN_INTERVAL,
    WHITE, WIDTH, YELLOW,
)
from utils import (
    init_mixer, load_assets, load_highscore, load_sounds, save_highscore,
    start_music,
)

# Game phases. Keeping them explicit removes the old blocking "game over"
# loop, so the window stays responsive on every screen.
PLAYING, PAUSED, GAME_OVER = "playing", "paused", "game_over"


def init_game(headless=False):
    """Start pygame and build the window, assets, sounds and fonts.

    None of this happens at import time any more: importing this module used
    to call pygame.init(), open a window and start music, which made the game
    impossible to test and loaded assets before set_mode() — the ordering that
    prevented every surface from being convert()ed.
    """
    pygame.init()
    init_mixer()

    flags = pygame.HIDDEN if headless else 0
    win = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("Space Shooter")

    # Assets load *after* set_mode so they can be converted to the display
    # format, and fall back to generated art when a file is missing.
    assets = load_assets()
    sounds = load_sounds()
    fonts = {
        "small": pygame.font.Font(None, 32),
        "medium": pygame.font.Font(None, 44),
        "large": pygame.font.Font(None, 72),
    }
    return win, assets, sounds, fonts


def draw_hud(win, fonts, state):
    for i, text in enumerate(
        (f"Score: {state.score}", f"Level: {state.level}", f"High Score: {state.high_score}")
    ):
        win.blit(fonts["small"].render(text, True, WHITE), (10, 10 + i * 30))
    if state.combo > 1:
        win.blit(
            fonts["small"].render(f"Combo x{state.combo}", True, YELLOW),
            (WIDTH - 150, 10),
        )


def draw_centered(win, font, text, y, color=WHITE):
    surface = font.render(text, True, color)
    win.blit(surface, (WIDTH // 2 - surface.get_width() // 2, y))


def redraw(win, assets, fonts, state, phase, now):
    win.blit(assets["background"], (0, 0))
    state.spaceship.draw(win, now)
    state.spaceship.draw_health_bar(win)

    for bullet in state.bullets:
        bullet.draw(win)
    for enemy in state.enemies:
        enemy.draw(win)
    for power_up in state.power_ups:
        power_up.draw(win)
    for explosion in state.explosions:
        explosion.draw(win)
    if state.boss:
        state.boss.draw(win)

    draw_hud(win, fonts, state)

    if phase == PAUSED:
        draw_centered(win, fonts["large"], "PAUSED", HEIGHT // 2 - 60)
        draw_centered(win, fonts["small"], "Press P to resume", HEIGHT // 2 + 20)
    elif phase == GAME_OVER:
        draw_centered(win, fonts["large"], "GAME OVER", HEIGHT // 2 - 150)
        draw_centered(win, fonts["medium"], f"Score: {state.score}", HEIGHT // 2 - 50)
        draw_centered(win, fonts["medium"], f"Level: {state.level}", HEIGHT // 2)
        draw_centered(win, fonts["medium"], f"High Score: {state.high_score}", HEIGHT // 2 + 50)
        draw_centered(win, fonts["small"], "Press R to restart, ESC to quit", HEIGHT // 2 + 150)

    pygame.display.update()


def update(state, sounds, dt, now):
    """Advance one frame of play. Sets state.game_over instead of restarting.

    Restarting is handled by the caller once iteration has finished, which is
    what the old code got wrong: it rebuilt the entity lists inside the enemy
    loop, so the next remove() hit a list that no longer held the item.
    """
    ship = state.spaceship

    for bullet in state.bullets[:]:
        bullet.move(dt)
        if bullet.rect.bottom < 0:
            state.bullets.remove(bullet)

    for explosion in state.explosions[:]:
        if explosion.update(dt):
            state.explosions.remove(explosion)

    killed_bullets = set()

    for enemy in state.enemies[:]:
        enemy.move(dt)

        if enemy.rect.top > HEIGHT:
            state.enemies.remove(enemy)
            state.combo = 1
            continue

        if enemy.rect.colliderect(ship.rect):
            if ship.take_damage(ENEMY_CONTACT_DAMAGE, now):
                state.add_explosion(enemy.rect.centerx, enemy.rect.centery)
                sounds["explosion"].play()
                state.enemies.remove(enemy)
                state.combo = 1
                if ship.health <= 0:
                    state.game_over = True
                    return
            continue

        for bullet in state.bullets:
            if id(bullet) in killed_bullets:
                continue
            if bullet.rect.colliderect(enemy.rect):
                killed_bullets.add(id(bullet))
                state.enemies.remove(enemy)
                state.add_explosion(enemy.rect.centerx, enemy.rect.centery)
                state.score += ENEMY_SCORE * state.combo
                state.combo += 1
                sounds["explosion"].play()
                if state.combo % COMBO_UPGRADE_STEP == 0:
                    ship.upgrade_weapon()
                break

    if killed_bullets:
        state.bullets[:] = [b for b in state.bullets if id(b) not in killed_bullets]

    if state.boss:
        state.boss.move(dt)
        if state.boss.rect.colliderect(ship.rect):
            if ship.take_damage(BOSS_CONTACT_DAMAGE, now):
                sounds["explosion"].play()
                if ship.health <= 0:
                    state.game_over = True
                    return
        for bullet in state.bullets[:]:
            if bullet.rect.colliderect(state.boss.rect):
                state.boss.health -= BOSS_BULLET_DAMAGE
                state.bullets.remove(bullet)
                if state.boss.health <= 0:
                    state.add_explosion(state.boss.rect.centerx, state.boss.rect.centery)
                    sounds["explosion"].play()
                    state.boss = None
                    state.score += BOSS_SCORE
                    state.advance_level()
                    break

    for power_up in state.power_ups[:]:
        power_up.move(dt)
        if power_up.rect.colliderect(ship.rect):
            ship.power_up(now)
            state.power_ups.remove(power_up)
            sounds["powerup"].play()
        elif power_up.rect.top > HEIGHT:
            state.power_ups.remove(power_up)

    # Time-based rather than per-frame, so the spawn rate does not depend on
    # how fast the machine renders.
    if random.random() < dt / POWERUP_SPAWN_INTERVAL:
        state.spawn_power_up()

    if not state.enemies and not state.boss:
        state.advance_level()

    ship.check_power_up(now)


def main(headless=False, max_frames=None):
    """Run the game. headless/max_frames exist so tests can drive the loop."""
    win, assets, sounds, fonts = init_game(headless=headless)
    start_music()

    state = GameState(assets, high_score=load_highscore())
    clock = pygame.time.Clock()
    phase = PLAYING
    running = True
    frames = 0

    try:
        while running:
            # Seconds since the last frame; capped so a stall (window drag,
            # breakpoint) cannot teleport everything across the screen.
            dt = min(clock.tick(FPS) / 1000.0, 0.05)
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_p and phase in (PLAYING, PAUSED):
                        phase = PAUSED if phase == PLAYING else PLAYING
                    elif event.key == pygame.K_r and phase == GAME_OVER:
                        state.reset()
                        phase = PLAYING

            if phase == PLAYING:
                keys = pygame.key.get_pressed()
                dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
                dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
                if dx or dy:
                    state.spaceship.move(dx, dy, dt)
                if keys[pygame.K_SPACE] and state.fire(now):
                    sounds["shoot"].play()

                update(state, sounds, dt, now)

                if state.game_over:
                    if state.record_high_score():
                        save_highscore(state.high_score)
                    phase = GAME_OVER

            redraw(win, assets, fonts, state, phase, now)

            frames += 1
            if max_frames is not None and frames >= max_frames:
                running = False
    finally:
        # Reached however the loop exits, including quitting from the game-over
        # screen — the old code returned early and skipped pygame.quit().
        if state.record_high_score():
            save_highscore(state.high_score)
        pygame.quit()

    return state


if __name__ == "__main__":
    main()
