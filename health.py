import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH

BAR_WIDTH = 200
BAR_HEIGHT = 20


class HealthContainer(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthContainer, self).__init__()
        self.surf = pygame.Surface((BAR_WIDTH, BAR_HEIGHT))
        self.surf.fill((100, 116, 139))
        self.rect = self.surf.get_rect()
        self.rect.left = SCREEN_WIDTH - BAR_WIDTH - 10
        self.rect.bottom = SCREEN_HEIGHT - 10


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthBar, self).__init__()
        self.update(1)

    def update(self, health):
        self.surf = pygame.Surface((BAR_WIDTH * health, BAR_HEIGHT))
        if health > 0.8:  # green
            self.surf.fill((22, 168, 74))
        elif health > 0.25:  # blue
            self.surf.fill((37, 99, 235))
        else:  # color bar in red
            self.surf.fill((225, 29, 72))

        self.rect = self.surf.get_rect()
        self.rect.left = SCREEN_WIDTH - BAR_WIDTH - 10
        self.rect.bottom = SCREEN_HEIGHT - 10
