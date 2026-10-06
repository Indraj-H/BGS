"""
Mario-style Platformer with Side Scrolling + Moving Platforms + Collectible Coins + Simple Enemy.
Fixed indentation errors.
"""

import pygame
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8#was 0.6
JUMP_POWER = 12
PLAYER_SPEED = 5

WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)
RED = (200, 50, 50)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Platformer")
clock = pygame.time.Clock()

score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.standing_platform = None

    def update(self, keys, platforms):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED

        self.vel_y += GRAVITY
        dy = self.vel_y

        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

        self.rect.y += dy
        self.on_ground = False
        self.standing_platform = None
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.standing_platform = platform
                elif dy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        if self.standing_platform and self.standing_platform.move_range > 0:
            self.rect.y += self.standing_platform.direction * self.standing_platform.speed

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_POWER

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, move_range=0, speed=0):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_y = y
        self.move_range = move_range
        self.speed = speed
        self.direction = 1

    def update(self):
        if self.move_range > 0:
            self.rect.y += self.direction * self.speed
            if self.rect.y > self.start_y + self.move_range or self.rect.y < self.start_y:
                self.direction *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, move_range=50, speed=2):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.move_range = move_range
        self.speed = speed
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.x > self.start_x + self.move_range or self.rect.x < self.start_x - self.move_range:
            self.direction *= -1

level_length = 1600
platforms = pygame.sprite.Group()
level_data = [
    (0, HEIGHT - 40, level_length, 40, 0, 0),
    (250, 500, 120, 20, 40, 1),
    (450, 450, 120, 20, 0, 0),
    (650, 400, 120, 20, 30, 1),
    (850, 350, 120, 20, 0, 0),
    (1050, 300, 120, 20, 0, 0)
]
for data in level_data:
    platforms.add(Platform(*data))

coins = pygame.sprite.Group()
coins.add(Coin(270, 470), Coin(480, 420), Coin(870, 320), Coin(1070, 270))

enemies = pygame.sprite.Group()
enemies.add(Enemy(500, HEIGHT - 80, 100), Enemy(900, HEIGHT - 80, 150))

player = Player(50, HEIGHT - 100)
scroll_x = 0

def main():
    global scroll_x, score
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    player.jump()

        keys = pygame.key.get_pressed()
        for p in platforms:
            p.update()
        for e in enemies:
            e.update()
        player.update(keys, platforms)

        # --- Coin Collection ---
        for coin in coins.copy():
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                score += 1

        # --- Enemy Collision ---
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                print("Game Over! Final Score:", score)
                pygame.quit()
                sys.exit()

        # --- Camera Scroll ---
        if player.rect.centerx - scroll_x > WIDTH * 0.6:
            scroll_x = player.rect.centerx - WIDTH * 0.6
        if player.rect.centerx - scroll_x < WIDTH * 0.4:
            scroll_x = player.rect.centerx - WIDTH * 0.4
        scroll_x = max(0, min(scroll_x, level_length - WIDTH))

        # --- Draw Everything ---
        win.fill(WHITE)
        for p in platforms:
            win.blit(p.image, (p.rect.x - scroll_x, p.rect.y))
        for coin in coins:
            win.blit(coin.image, (coin.rect.x - scroll_x, coin.rect.y))
        for enemy in enemies:
            win.blit(enemy.image, (enemy.rect.x - scroll_x, enemy.rect.y))
        win.blit(player.image, (player.rect.x - scroll_x, player.rect.y))

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        win.blit(score_text, (10, 10))

        pygame.display.update()

if __name__ == "__main__":
    main()

