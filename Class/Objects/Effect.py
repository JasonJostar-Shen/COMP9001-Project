import pygame
from Utils.Setting import EFFECT_TYPE

class Effect(pygame.sprite.Sprite):
    def __init__(self,eType,pos,frame,text=None,fontsize=15,fontColor=(255,255,255),url=None):
        super().__init__()
        if url != None: self.image = pygame.image.load(url).convert_alpha()
        if text != None:
            self.font = pygame.font.SysFont("arial", fontsize)
            self.image = self.font.render(text, True, fontColor)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.eType = eType
        self.frame = frame
    
    def update(self):
        if self.eType not in EFFECT_TYPE: return
        if self.eType == EFFECT_TYPE[0]:
            alpha = self.image.get_alpha()
            if alpha == 0:
                self.kill()
            else:
                alpha -= 255//self.frame
                alpha = alpha if alpha > 0 else 0
                self.image.set_alpha(alpha)
        elif self.eType == EFFECT_TYPE[1]:
            alpha = self.image.get_alpha()
            if alpha == 0:
                self.kill()
            else:
                alpha -= 255//self.frame
                alpha = alpha if alpha > 0 else 0
                self.image.set_alpha(alpha)
            self.rect.y -= 1