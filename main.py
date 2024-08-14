import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load assets
SPACESHIP_IMAGE = pygame.image.load("assets/spaceship.png")
BULLET_IMAGE = pygame.image.load("assets/bullet.png")
ENEMY_IMAGE = pygame.image.load("assets/enemy.png")
BACKGROUND = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))

# Define colors
WHITE = (255, 255, 255)

# Game settings
FPS = 60
SPACESHIP_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2

class Spaceship:
    def __init__(self, x, y):
        self.image = SPACESHIP_IMAGE
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, win):
        win.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, win):
        win.blit(self.image, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.image = ENEMY_IMAGE
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.rect.y += ENEMY_SPEED

    def draw(self, win):
        win.blit(self.image, self.rect)

def main():
    clock = pygame.time.Clock()
    run = True

    spaceship = Spaceship(WIDTH//2, HEIGHT - 50)
    bullets = []
    enemies = []
    score = 0

    def redraw_window():
        WIN.blit(BACKGROUND, (0, 0))
        spaceship.draw(WIN)
        for bullet in bullets:
            bullet.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)

        # Display score
        score_text = pygame.font.SysFont("comicsans", 30).render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))

        pygame.display.update()

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
            bullets.append(Bullet(spaceship.rect.centerx, spaceship.rect.top))

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        if random.randint(1, 20) == 1:
            enemies.append(Enemy(random.randint(20, WIDTH - 20), 0))

        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
            if enemy.rect.colliderect(spaceship.rect):
                spaceship.health -= 10
                enemies.remove(enemy)
            for bullet in bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10

        redraw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
