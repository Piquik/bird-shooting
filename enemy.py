import pygame
import random
from pygame import RLEACCEL

from config import SCREEN_HEIGHT, SCREEN_WIDTH

# Define the enemy object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("mouche.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(2, 8)

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
