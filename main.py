# Import the pygame module
from time import sleep
import pygame
from cloud import Cloud
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from sound import collision_sound

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from enemy import Enemy
from events import ADD_CLOUD, ADD_ENEMY

from player import Player


# Initialize pygame
pygame.init()

# Setup for sounds. Defaults are good.
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(loops=-1)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering

# enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Add a new enemy every 250ms
pygame.time.set_timer(ADD_ENEMY, 250)

# Add a new cloud every second (1000ms)
pygame.time.set_timer(ADD_CLOUD, 1000)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue (including custom events)
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False

        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        if event.type == ADD_CLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        if event.type == ADD_ENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update the sprites
    clouds.update()
    enemies.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()

        collision_sound.play()
        sleep(3)
        # Stop the loop
        running = False

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
