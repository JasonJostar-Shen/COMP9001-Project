import pygame
from Utils.Setting import EFFECT_TYPE

class Effect(pygame.sprite.Sprite):
    def __init__(self,eType,pos,url=None):
        super().__init__()
        if url != None: self.image = pygame.image.load(url).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.eType = eType
    
    def update(self):
        if self.eType not in EFFECT_TYPE: return
        if self.eType == EFFECT_TYPE[0]:
            alpha = self.image.get_alpha()
            if alpha == 0:
                self.kill()
            else:
                alpha -= 20
                alpha = alpha if alpha > 0 else 0
                self.image.set_alpha(alpha)