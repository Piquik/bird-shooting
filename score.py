import pygame
from config import SCREEN_HEIGHT


class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.update(0)

    def update(self, score):
        self.surf = pygame.font.Font(None, 50).render(str(score), True, (0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.left = 10
        self.rect.bottom = SCREEN_HEIGHT - 10
