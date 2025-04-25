import pygame
from Utils.Setting import WIDTH,HEIGHT

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH,50))
        self.image.fill((160,160,160))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0,HEIGHT-40)