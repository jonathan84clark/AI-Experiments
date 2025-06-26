import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter with Upgrades")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Load assets
FONT = pygame.font.Font(None, 36)

# Spaceship class
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.weapon_level = 1  # Determines weapon type

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

        # Keep the spaceship on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        bullets = []
        if self.weapon_level == 1:
            bullets.append(Bullet(self.rect.right, self.rect.centery))
        elif self.weapon_level == 2:  # Twin blasters
            bullets.append(Bullet(self.rect.right, self.rect.top + 5))
            bullets.append(Bullet(self.rect.right, self.rect.bottom - 5))
        elif self.weapon_level == 3:  # Missiles
            bullets.append(Missile(self.rect.right, self.rect.centery))
        return bullets

# NPC class
class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.randint(3, 7)

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 10

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 7

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Upgrade class
class Upgrade(pygame.sprite.Sprite):
    def __init__(self, x, y, upgrade_type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.upgrade_type = upgrade_type

        if upgrade_type == 2:
            self.image.fill(YELLOW)  # Twin blasters
        elif upgrade_type == 3:
            self.image.fill(PURPLE)  # Missiles

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += 2
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
npсs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
upgrades = pygame.sprite.Group()

# Create the player
player = SpaceShip()
all_sprites.add(player)

# Game variables
score = 0
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for bullet in player.shoot():
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Spawn NPCs
    if random.random() < 0.02:
        npc = NPC()
        all_sprites.add(npc)
        npсs.add(npc)

    # Drop upgrades randomly when an NPC is destroyed
    for bullet in bullets:
        hit_npcs = pygame.sprite.spritecollide(bullet, npсs, True)
        for hit in hit_npcs:
            score += 1
            bullet.kill()
            if random.random() < 0.3:  # 30% chance to drop an upgrade
                upgrade_type = random.choice([2, 3])  # Twin blasters or Missiles
                upgrade = Upgrade(hit.rect.centerx, hit.rect.centery, upgrade_type)
                all_sprites.add(upgrade)
                upgrades.add(upgrade)

    # Check for player collecting upgrades
    collected_upgrades = pygame.sprite.spritecollide(player, upgrades, True)
    for upgrade in collected_upgrades:
        player.weapon_level = max(player.weapon_level, upgrade.upgrade_type)

    # Update
    all_sprites.update()

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Flip the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
