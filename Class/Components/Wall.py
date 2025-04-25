import pygame
from Utils.Setting import HEIGHT,WALL_URL

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        texture = pygame.image.load(WALL_URL).convert()
        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0,HEIGHT-40)