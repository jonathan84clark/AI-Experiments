import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
TILE_SIZE = 20
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Maze layout (1 = wall, 0 = empty, 2 = dot)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2, 1],
    [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 2, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 1, 2, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Player setup
player_pos = [1, 1]
player_speed = 2

# Draw maze
def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif maze[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), 5)

# Move player
def move_player(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    # Check collisions with walls
    if maze[new_y // TILE_SIZE][new_x // TILE_SIZE] != 1:
        player_pos[0] = new_x
        player_pos[1] = new_y

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move_player(0, -player_speed)
    if keys[pygame.K_DOWN]:
        move_player(0, player_speed)
    if keys[pygame.K_LEFT]:
        move_player(-player_speed, 0)
    if keys[pygame.K_RIGHT]:
        move_player(player_speed, 0)

    # Check for dot collection
    player_tile_x = player_pos[0] // TILE_SIZE
    player_tile_y = player_pos[1] // TILE_SIZE
    if maze[player_tile_y][player_tile_x] == 2:
        maze[player_tile_y][player_tile_x] = 0

    # Draw maze and player
    draw_maze()
    pygame.draw.circle(screen, YELLOW, (player_pos[0] + TILE_SIZE // 2, player_pos[1] + TILE_SIZE // 2), TILE_SIZE // 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()