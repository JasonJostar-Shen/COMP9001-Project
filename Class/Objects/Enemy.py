import pygame
import random
import Utils.GameUtils as GU
from Utils.Setting import WIDTH,ENEMY_IMG_URL
from Class.Components.ProgressBar import ProgressBar

class Enemy(pygame.sprite.Sprite):
    def __init__(self,hp,speed,url,score,expParam):
        self.hp = hp
        self.speed = speed
        self.exp = GU.CalEnemyExp(self.hp,expParam)
        self.score = score
        self.url = url
        super().__init__()

        self.image = pygame.image.load(url).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(self.rect.width, WIDTH - self.rect.width),-self.rect.height)
        self.y = self.rect.y
        # self.mask = pygame.mask.from_surface(self.image)
        self.lifeBar = ProgressBar(self.image.get_width(),6,self.getLifeBarCenter(),self.hp,5)

    def update(self,isFast):
        self.y += self.speed * 2 if isFast else self.speed
        self.rect.y = int(self.y)
        alpha = self.image.get_alpha()
        if alpha != 255: self.image.set_alpha(alpha+5)
        self.lifeBar.setValue(self.hp)
        self.lifeBar.update(self.getLifeBarCenter())
    
    def takenDamage(self,damage:int):
        self.hp -= damage
        self.image.set_alpha(180)
    
    def isDead(self):
        return self.hp <= 0
    
    def getLifeBarCenter(self):
        return (self.rect.midtop[0],self.rect.midtop[1]-5)
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        self.lifeBar.draw(screen)
        