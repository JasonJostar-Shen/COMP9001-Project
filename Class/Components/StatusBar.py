import pygame
from Utils.Setting import STATUSWIDTH,HEIGHT,WIDTH
from Class.Objects.Player import Player
class StatusBar:
    def __init__(self,player:Player):
        self.player = player
        self.width = STATUSWIDTH
        self.color = (150,150,0)
        self.front = pygame.font.SysFont(None,20)
        self.surface = pygame.Surface((self.width,HEIGHT),pygame.SRCALPHA)
        self.surface.set_alpha(200)
        self.rect = self.surface.get_rect(topleft=(WIDTH,0))
    
    def update(self,screen):
        self.surface.fill(self.color)
        # lvText = self.front.render(f"LV: {self.player.lv}",True,(0,0,0))
        # hpText = self.front.render(f"HP: {self.player.hp}",True,(0,0,0))
        # expText = self.front.render(f"Exp: {self.player.exp}/{self.player.getLvGap()}",True,(0,0,0))
        
        # self.surface.blit(hpText,(5,10))
        # self.surface.blit(expText,(5,40))
        self.updateText()
        screen.blit(self.surface,self.rect.topleft)

    def updateText(self):
        leftTopGap = (5,10)
        interval = 30
        texts = []
        texts.append(self.front.render(f"LV: {self.player.lv}",True,(0,0,0)))
        texts.append(self.front.render(f"HP: {self.player.hp}",True,(0,0,0)))
        texts.append(self.front.render(f"Exp: {self.player.exp}/{self.player.getLvGap()}",True,(0,0,0)))
        texts.append(self.front.render(f"AS: {self.player.attackSpeed/1000.0:.1f}s",True,(0,0,0)))
        texts.append(self.front.render(f"ATK: {self.player.atk}",True,(0,0,0)))
        for i in range(len(texts)):
            self.surface.blit(texts[i],(leftTopGap[0],leftTopGap[1]+i*interval))
