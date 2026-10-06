import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 650, 600  # ✅ Narrower screen (was 800x600)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - 1-Hit Kill Edition")
FONT = pygame.font.SysFont("consolas", 24)
BIGFONT = pygame.font.SysFont("consolas", 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (40, 130, 230)
BULLET_COLOR = (200, 255, 200)
ENEMY_COLORS = {"small": (220, 60, 60), "medium": (220, 140, 60), "large": (180, 60, 220)}
POWERUP_COLORS = {"health": (100, 255, 100), "rapid": (100, 200, 255), "shield": (255, 255, 100)}

clock = pygame.time.Clock()
FPS = 60

# ================= Difficulty Settings =================
DIFFICULTY_SETTINGS = {
    "Easy": {"lives": 5, "spawn_interval": 50, "drop_chance": 0.5},
    "Normal": {"lives": 3, "spawn_interval": 35, "drop_chance": 0.4},
    "Hard": {"lives": 2, "spawn_interval": 20, "drop_chance": 0.3},
}
# =======================================================


class Player:
    def __init__(self, lives):
        self.w, self.h = 50, 36
        self.rect = pygame.Rect(WIDTH // 2 - self.w // 2, HEIGHT - self.h - 12, self.w, self.h)
        self.speed = 6
        self.lives = lives
        self.score = 0
        self.last_shot = 0
        self.cooldown = 250  # ms

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def can_shoot(self, now):
        return now - self.last_shot >= self.cooldown

    def shoot(self, now):
        self.last_shot = now
        return Bullet(self.rect.centerx, self.rect.top)

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 3, y - 8, 6, 12)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, BULLET_COLOR, self.rect)


class Enemy:
    def __init__(self, x, y, entype):
        self.entype = entype
        if entype == "small":
            self.w, self.h, self.speed = 36, 26, 3
        elif entype == "medium":
            self.w, self.h, self.speed = 46, 34, 2
        else:
            self.w, self.h, self.speed = 62, 46, 1.5

        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.hp = 1  # ✅ Always 1-hit kill

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLORS[self.entype], self.rect)


class PowerUp:
    def __init__(self, x, y, ptype):
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        self.ptype = ptype
        self.speed = 2

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, POWERUP_COLORS[self.ptype], self.rect)
        s = FONT.render(self.ptype[0].upper(), True, BLACK)
        WIN.blit(s, (self.rect.x + 4, self.rect.y))


def choose_difficulty():
    difficulties = list(DIFFICULTY_SETTINGS.keys())
    selected = 0
    while True:
        WIN.fill(BLACK)
        title = BIGFONT.render("Choose Difficulty", True, WHITE)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        for i, d in enumerate(difficulties):
            color = WHITE if i != selected else (255, 200, 50)
            txt = FONT.render(d, True, color)
            WIN.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 250 + i * 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    return difficulties[selected]


def main():
    difficulty = choose_difficulty()
    settings = DIFFICULTY_SETTINGS[difficulty]

    player = Player(lives=settings["lives"])
    bullets, enemies = [], []
    spawn_counter = 0
    running = True

    while running:
        clock.tick(FPS)
        spawn_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_SPACE] and player.can_shoot(pygame.time.get_ticks()):
            bullets.append(player.shoot(pygame.time.get_ticks()))

        if spawn_counter >= settings["spawn_interval"]:
            spawn_counter = 0
            enemies.append(Enemy(random.randint(20, WIDTH - 60), -50,
                                 random.choice(["small", "medium", "large"])))

        for b in bullets[:]:
            b.update()
            if b.rect.bottom < 0:
                bullets.remove(b)

        for e in enemies[:]:
            e.update()
            if e.rect.top > HEIGHT:
                enemies.remove(e)
                player.lives -= 1
                if player.lives <= 0:
                    running = False

        # Bullet vs Enemy collisions
        for b in bullets[:]:
            for e in enemies[:]:
                if b.rect.colliderect(e.rect):
                    bullets.remove(b)
                    enemies.remove(e)
                    player.score += 10
                    break

        WIN.fill(BLACK)
        player.draw(WIN)
        for b in bullets:
            b.draw(WIN)
        for e in enemies:
            e.draw(WIN)

        score_text = FONT.render(f"Score: {player.score} | Lives: {player.lives} | Difficulty: {difficulty}", True, WHITE)
        WIN.blit(score_text, (10, 10))
        pygame.display.update()


if __name__ == "__main__":
    main()
