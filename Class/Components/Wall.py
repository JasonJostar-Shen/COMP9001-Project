import pygame
from Utils.Setting import WIDTH,HEIGTH

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH,40))
        self.image.fill((160,160,160))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,HEIGTH-40)