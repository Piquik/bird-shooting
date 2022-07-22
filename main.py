# Import the pygame module
from re import L
from time import sleep
import pygame
from cloud import Cloud
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from health import HealthBar, HealthContainer
from package import Package
from score import Score
from sound import collision_sound, enemy_explode, laser_sound

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)
from enemy import Enemy
from events import ADD_CLOUD, ADD_ENEMY, ADD_PACKAGE
from player import Player
from package import Package

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
clouds = pygame.sprite.Group()
enemies = pygame.sprite.Group()
lasers = pygame.sprite.Group()
packages = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Add a score text object to all_sprites
score = Score()
all_sprites.add(score)

# Add a health bar
health_container = HealthContainer()
all_sprites.add(health_container)
health_bar = HealthBar()
all_sprites.add(health_bar)

# Add a new enemy every 250ms
pygame.time.set_timer(ADD_ENEMY, 250)

# Add a new cloud every second (1000ms)
pygame.time.set_timer(ADD_CLOUD, 1000)


# Add a new gift every 10 seconds (10000ms)
pygame.time.set_timer(ADD_PACKAGE, 10000)

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

            if event.key == K_SPACE:
                laser = player.shoot()
                lasers.add(laser)
                all_sprites.add(laser)
                laser_sound.play()

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

        if event.type == ADD_PACKAGE:
            new_package = Package()
            packages.add(new_package)
            all_sprites.add(new_package)

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update the sprites
    clouds.update()
    enemies.update()
    lasers.update()
    packages.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Check if any enemies have collided with the player
    enemy_colision = pygame.sprite.spritecollideany(player, enemies)
    if enemy_colision:
        # If so, then remove the player and stop the loop
        # player.kill()
        player.hit(10)
        health_bar.update(player.health / 100)
        collision_sound.play()
        enemy_colision.kill()

        if not player.alive:
            sleep(3)
            # Stop the loop
            running = False

    # Check if any lasers have collided with an enemy
    for laser in lasers:
        collided = pygame.sprite.spritecollideany(laser, enemies)
        if collided:
            laser.kill()
            collided.kill()
            enemy_explode.play()
            player.score += 1
            score.update(player.score)

    package_colision = pygame.sprite.spritecollideany(player, packages)
    if package_colision:
        package_colision.kill()
        player.health_boost()
        health_bar.update(player.health / 100)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
