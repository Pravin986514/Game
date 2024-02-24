import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 20
FRIEND_SIZE = 20
FRIEND_SPAWN_RATE = 50
PLAYER_SPEED = 5
FRIEND_SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Conga Line")

# Load character assets
player_image = pygame.image.load('character_sheet.png')
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
friend_image = pygame.Surface((FRIEND_SIZE, FRIEND_SIZE))
friend_image.fill(RED)

clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.direction = 'right'
        self.conga_line = []

    def move(self):
        if self.direction == 'up':
            self.y -= PLAYER_SPEED
        elif self.direction == 'down':
            self.y += PLAYER_SPEED
        elif self.direction == 'left':
            self.x -= PLAYER_SPEED
        elif self.direction == 'right':
            self.x += PLAYER_SPEED

    def draw(self):
        screen.blit(player_image, (self.x, self.y))
        for follower in self.conga_line:
            screen.blit(friend_image, (follower.x, follower.y))

class Friend:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, target_x, target_y):
        if self.x < target_x:
            self.x += FRIEND_SPEED
        elif self.x > target_x:
            self.x -= FRIEND_SPEED
        if self.y < target_y:
            self.y += FRIEND_SPEED
        elif self.y > target_y:
            self.y -= FRIEND_SPEED

    def draw(self):
        screen.blit(friend_image, (self.x, self.y))

# Initialize player
player = Player()

# Game loop
running = True
score = 0
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.direction = 'up'
            elif event.key == pygame.K_DOWN:
                player.direction = 'down'
            elif event.key == pygame.K_LEFT:
                player.direction = 'left'
            elif event.key == pygame.K_RIGHT:
                player.direction = 'right'

    # Move player
    player.move()

    # Check collisions with edges
    if player.x < 0 or player.x >= SCREEN_WIDTH or player.y < 0 or player.y >= SCREEN_HEIGHT:
        running = False

    # Spawn friend randomly
    if random.randint(1, FRIEND_SPAWN_RATE) == 1:
        friend = Friend(random.randint(0, SCREEN_WIDTH - FRIEND_SIZE), random.randint(0, SCREEN_HEIGHT - FRIEND_SIZE))

    # Move friend towards player
    if 'friend' in locals():
        friend.move_towards(player.x, player.y)

        # Check collision with player
        if player.x < friend.x + FRIEND_SIZE and player.x + PLAYER_SIZE > friend.x and player.y < friend.y + FRIEND_SIZE and player.y + PLAYER_SIZE > friend.y:
            player.conga_line.append(friend)
            score += 1
            del friend

    # Draw player and friends
    player.draw()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
