import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids with Mouse Control")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Load spaceship image
SPACESHIP_IMAGE = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.polygon(SPACESHIP_IMAGE, WHITE, [(25, 50), (0, 0), (25, 15), (50, 0)])  # Rotated 90° left

class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.speed = 5
        self.alive = True
        self.immune = False
        self.immune_start_time = None

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))

        # Handle immunity timer
        if self.immune and time.time() - self.immune_start_time > 5:
            self.immune = False

    def draw(self):
        if self.alive:
            rotated_image = pygame.transform.rotate(SPACESHIP_IMAGE, -self.angle)
            rect = rotated_image.get_rect(center=(self.x, self.y))
            screen.blit(rotated_image, rect.topleft)

            # Draw immunity indicator
            if self.immune:
                pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 60, 2)

    def get_front_position(self):
        front_x = self.x + 25 * math.cos(math.radians(self.angle))
        front_y = self.y + 25 * math.sin(math.radians(self.angle))
        return front_x, front_y

    def hit(self):
        if not self.immune:
            self.alive = False

    def respawn(self):
        self.alive = True
        self.immune = True
        self.immune_start_time = time.time()

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.speed = 10
        self.radius = 5

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    def off_screen(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

class Asteroid:
    def __init__(self, x=None, y=None, radius=None):
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 3)
        self.radius = radius if radius is not None else random.randint(40, 80)
        self.shape_type = random.choice(["circle", "triangle"])
        self.color = [random.randint(50, 255) for _ in range(3)]

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Wrap around screen
        if self.x < 0: self.x = WIDTH
        if self.x > WIDTH: self.x = 0
        if self.y < 0: self.y = HEIGHT
        if self.y > HEIGHT: self.y = 0

    def draw(self):
        if self.shape_type == "circle":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        elif self.shape_type == "triangle":
            points = [
                (self.x + self.radius * math.cos(self.angle), self.y + self.radius * math.sin(self.angle)),
                (self.x + self.radius * math.cos(self.angle + 2 * math.pi / 3), self.y + self.radius * math.sin(self.angle + 2 * math.pi / 3)),
                (self.x + self.radius * math.cos(self.angle + 4 * math.pi / 3), self.y + self.radius * math.sin(self.angle + 4 * math.pi / 3))
            ]
            pygame.draw.polygon(screen, self.color, points)

    def split(self):
        if self.radius > 20:
            return [
                Asteroid(self.x, self.y, self.radius // 2),
                Asteroid(self.x, self.y, self.radius // 2)
            ]
        return []

    def bounce(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        if distance < self.radius + other.radius:
            # Calculate angle of collision
            angle = math.atan2(other.y - self.y, other.x - self.x)

            # Swap velocities
            self.angle, other.angle = other.angle, self.angle

            # Push asteroids apart to prevent sticking
            overlap = self.radius + other.radius - distance
            self.x -= math.cos(angle) * overlap / 2
            self.y -= math.sin(angle) * overlap / 2
            other.x += math.cos(angle) * overlap / 2
            other.y += math.sin(angle) * overlap / 2

# Game objects
spaceship = Spaceship()
bullets = []
asteroids = [Asteroid() for _ in range(5)]

# Button class for respawn
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

respawn_button = Button("Respawn", WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)

# Score
score = 0

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and spaceship.alive:
            if event.button == 1:  # Left mouse button
                bullet_x, bullet_y = spaceship.get_front_position()
                bullets.append(Bullet(bullet_x, bullet_y, spaceship.angle))

        if not spaceship.alive and respawn_button.is_clicked(event):
            spaceship.respawn()

    if spaceship.alive:
        # Update
        spaceship.update()

        for bullet in bullets:
            bullet.update()

        for asteroid in asteroids:
            asteroid.update()

        # Check for collisions
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                distance = math.hypot(bullet.x - asteroid.x, bullet.y - asteroid.y)
                if distance < asteroid.radius:
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    asteroids.extend(asteroid.split())
                    score += 1  # Increase score
                    break

            if bullet.off_screen():
                bullets.remove(bullet)

        for asteroid in asteroids:
            distance = math.hypot(spaceship.x - asteroid.x, spaceship.y - asteroid.y)
            if distance < asteroid.radius:
                spaceship.hit()

        # Ensure asteroids are endless
        while len(asteroids) < 5:
            asteroids.append(Asteroid())

        # Handle asteroid-asteroid collisions
        for i, asteroid1 in enumerate(asteroids):
            for asteroid2 in asteroids[i + 1:]:
                asteroid1.bounce(asteroid2)

        # Draw
        spaceship.draw()

        for bullet in bullets:
            bullet.draw()

        for asteroid in asteroids:
            asteroid.draw()

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        respawn_button.draw()

    # Refresh screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
