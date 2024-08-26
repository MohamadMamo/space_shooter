# main.py

import pygame
import random
from settings import *
from utils import load_assets, load_sounds, load_highscore, save_highscore
from spaceship import Spaceship
from bullet import Bullet
from enemy import Enemy, Boss
from powerup import PowerUp
from explosion import Explosion

# Initialize Pygame
pygame.init()

# Load assets and sounds
assets = load_assets()
sounds = load_sounds()

# Screen setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

def main():
    clock = pygame.time.Clock()
    run = True

    spaceship = Spaceship(WIDTH // 2, HEIGHT - 50, assets)
    bullets = []
    enemies = []
    power_ups = []
    explosions = []
    boss = None
    score = 0
    high_score = load_highscore()
    level = 1
    combo = 1

    def redraw_window():
        WIN.blit(assets["background"], (0, 0))
        spaceship.draw(WIN)
        spaceship.draw_health_bar(WIN)

        for bullet in bullets:
            bullet.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        for power_up in power_ups:
            power_up.draw(WIN)
        for explosion in explosions[:]:
            if explosion.draw(WIN):
                explosions.remove(explosion)
        if boss:
            boss.draw(WIN)

        score_text = pygame.font.SysFont("comicsans", 40).render(f"Score: {score}", True, WHITE)
        level_text = pygame.font.SysFont("comicsans", 40).render(f"Level: {level}", True, WHITE)
        high_score_text = pygame.font.SysFont("comicsans", 40).render(f"High Score: {high_score}", True, WHITE)
        WIN.blit(score_text, (10, 10))
        WIN.blit(level_text, (10, 50))
        WIN.blit(high_score_text, (10, 90))

        pygame.display.update()

    def spawn_enemies():
        for _ in range(level * 5):
            enemies.append(Enemy(random.randint(20, WIDTH - 20), random.randint(-1500, -100), ENEMY_SPEED, assets))
        if level % 3 == 0:  # Add faster enemies every 3 levels
            enemies.append(Enemy(random.randint(20, WIDTH - 20), random.randint(-1500, -100), ENEMY_FAST_SPEED, assets))

    def spawn_boss():
        nonlocal boss
        boss = Boss(WIDTH // 2, 100, assets)

    def game_over_screen():
        nonlocal high_score
        if score > high_score:
            high_score = score
            save_highscore(high_score)

        game_over_text = pygame.font.SysFont("comicsans", 60).render("GAME OVER", True, WHITE)
        score_text = pygame.font.SysFont("comicsans", 40).render(f"Score: {score}", True, WHITE)
        level_text = pygame.font.SysFont("comicsans", 40).render(f"Level: {level}", True, WHITE)
        high_score_text = pygame.font.SysFont("comicsans", 40).render(f"High Score: {high_score}", True, WHITE)
        restart_text = pygame.font.SysFont("comicsans", 30).render("Press R to Restart", True, WHITE)

        WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
        WIN.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 150))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False
                    return True
            clock.tick(FPS)

    spawn_enemies()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship.move(-SPACESHIP_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            spaceship.move(SPACESHIP_SPEED, 0)
        if keys[pygame.K_UP]:
            spaceship.move(0, -SPACESHIP_SPEED)
        if keys[pygame.K_DOWN]:
            spaceship.move(0, SPACESHIP_SPEED)
        if keys[pygame.K_SPACE]:
            if spaceship.weapon_level == 1:
                bullets.append(Bullet(spaceship.rect.centerx, spaceship.rect.top, assets))
            elif spaceship.weapon_level == 2:
                bullets.append(Bullet(spaceship.rect.centerx - 10, spaceship.rect.top, assets))
                bullets.append(Bullet(spaceship.rect.centerx + 10, spaceship.rect.top, assets))
            elif spaceship.weapon_level == 3:
                bullets.append(Bullet(spaceship.rect.centerx, spaceship.rect.top, assets))
                bullets.append(Bullet(spaceship.rect.centerx - 20, spaceship.rect.top, assets))
                bullets.append(Bullet(spaceship.rect.centerx + 20, spaceship.rect.top, assets))
            sounds["shoot"].play()

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                combo = 1
            elif enemy.rect.colliderect(spaceship.rect):
                spaceship.health -= 10
                explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery, assets))
                enemies.remove(enemy)
                sounds["explosion"].play()
                if spaceship.health <= 0:
                    run = game_over_screen()
                    if not run:
                        return
                    else:
                        spaceship = Spaceship(WIDTH // 2, HEIGHT - 50, assets)
                        bullets = []
                        enemies = []
                        power_ups = []
                        explosions = []
                        boss = None
                        score = 0
                        level = 1
                        combo = 1
                        spawn_enemies()
            else:
                for bullet in bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        if enemy in enemies:
                            bullets.remove(bullet)
                            explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery, assets))
                            enemies.remove(enemy)
                            score += 10 * combo
                            combo += 1
                            sounds["explosion"].play()
                            if combo % 5 == 0:
                                spaceship.upgrade_weapon()

        if boss:
            boss.move()
            if boss.rect.colliderect(spaceship.rect):
                spaceship.health -= 20
                sounds["explosion"].play()
                if spaceship.health <= 0:
                    run = game_over_screen()
                    if not run:
                        return
                    else:
                        spaceship = Spaceship(WIDTH // 2, HEIGHT - 50, assets)
                        bullets = []
                        enemies = []
                        power_ups = []
                        explosions = []
                        boss = None
                        score = 0
                        level = 1
                        combo = 1
                        spawn_enemies()
            else:
                for bullet in bullets[:]:
                    if bullet.rect.colliderect(boss.rect):
                        boss.health -= 5
                        bullets.remove(bullet)
                        if boss.health <= 0:
                            explosions.append(Explosion(boss.rect.centerx, boss.rect.centery, assets))
                            boss = None
                            score += 500
                            level += 1
                            spawn_enemies()

        for power_up in power_ups[:]:
            power_up.move()
            if power_up.rect.colliderect(spaceship.rect):
                spaceship.power_up()
                power_ups.remove(power_up)
                sounds["powerup"].play()
            elif power_up.rect.top > HEIGHT:
                power_ups.remove(power_up)

        if random.randint(1, 300) == 1:
            power_ups.append(PowerUp(random.randint(20, WIDTH - 20), 0, assets))

        if len(enemies) == 0 and not boss:
            level += 1
            if level % 5 == 0:
                spawn_boss()
            else:
                spawn_enemies()

        spaceship.check_power_up()
        redraw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
