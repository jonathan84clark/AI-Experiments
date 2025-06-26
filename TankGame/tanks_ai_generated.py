import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Battle Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Tank attributes
tank_width, tank_height = 50, 30
tank_speed = 5

# Bullet attributes
bullet_width, bullet_height = 5, 10
bullet_speed = 10

# Enemy attributes
enemy_width, enemy_height = 50, 30
enemy_speed = 2
enemy_bullet_speed = 5

# Initialize the player's tank
tank_x = WIDTH // 2
tank_y = HEIGHT - tank_height - 10

# Bullet list
bullets = []

# Enemy list
enemies = []

# Enemy bullet list
enemy_bullets = []

# Font for score display
font = pygame.font.SysFont(None, 36)

# Score
score = 0

# Explosion effect
explosion_timer = 0
explosion_duration = 30
explosion_coords = None

# Respawn button
respawn_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)
respawn = False

def draw_tank(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, tank_width, tank_height))

def draw_bullet(bullet):
    pygame.draw.rect(screen, RED, bullet)

def draw_enemy(enemy):
    pygame.draw.rect(screen, GREEN, enemy)

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_explosion(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), 40)
    pygame.draw.circle(screen, RED, (x, y), 20)

def draw_respawn_button():
    pygame.draw.rect(screen, WHITE, respawn_button)
    text = font.render("Respawn", True, BLACK)
    screen.blit(text, (respawn_button.x + 50, respawn_button.y + 15))

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and respawn_button.collidepoint(event.pos) and explosion_timer == 0:
            respawn = True

    if respawn:
        tank_x = WIDTH // 2
        tank_y = HEIGHT - tank_height - 10
        respawn = False

    # Handle tank movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and tank_x > 0:
        tank_x -= tank_speed
    if keys[pygame.K_RIGHT] and tank_x < WIDTH - tank_width:
        tank_x += tank_speed
    if keys[pygame.K_SPACE] and explosion_timer == 0:
        # Fire a bullet
        if len(bullets) < 5:  # Limit the number of bullets on screen
            bullets.append(pygame.Rect(tank_x + tank_width // 2 - bullet_width // 2, tank_y, bullet_width, bullet_height))

    # Update bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Spawn enemies
    if random.randint(1, 100) <= 2:  # 2% chance to spawn an enemy per frame
        enemies.append(pygame.Rect(random.randint(0, WIDTH - enemy_width), 0, enemy_width, enemy_height))

    # Update enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
        else:
            # Enemy fires a bullet
            if random.randint(1, 100) <= 2:  # 2% chance to fire a bullet per frame
                enemy_bullets.append(pygame.Rect(enemy.x + enemy_width // 2 - bullet_width // 2, enemy.y + enemy_height, bullet_width, bullet_height))

        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1

    # Update enemy bullets
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.y += enemy_bullet_speed
        if enemy_bullet.y > HEIGHT:
            enemy_bullets.remove(enemy_bullet)
        elif enemy_bullet.colliderect(pygame.Rect(tank_x, tank_y, tank_width, tank_height)) and explosion_timer == 0:
            explosion_coords = (tank_x + tank_width // 2, tank_y + tank_height // 2)
            explosion_timer = explosion_duration
            enemy_bullets.remove(enemy_bullet)

    # Draw everything
    if explosion_timer > 0:
        draw_explosion(*explosion_coords)
        explosion_timer -= 1
        if explosion_timer == 0:
            draw_respawn_button()
    else:
        draw_tank(tank_x, tank_y)

    for bullet in bullets:
        draw_bullet(bullet)
    for enemy in enemies:
        draw_enemy(enemy)
    for enemy_bullet in enemy_bullets:
        draw_bullet(enemy_bullet)
    show_score()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()