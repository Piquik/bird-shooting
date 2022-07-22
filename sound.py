import pygame

pygame.mixer.init()

collision_sound = pygame.mixer.Sound("explosion.ogg")
enemy_explode = pygame.mixer.Sound("enemy_explode.ogg")
laser_sound = pygame.mixer.Sound("laser.mp3")

enemy_explode.set_volume(0.35)
