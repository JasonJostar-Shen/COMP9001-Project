import pygame
import random
import Utils.GameUtils as GU
from Utils.Setting import WIDTH,HEIGHT,ENEMY_INITHP,ENEMY_INITSPEED,ENEMY_IMG_URL

class Enemy(pygame.sprite.Sprite):
    def __init__(self,hp,speed):
        self.hp = hp
        self.speed = speed
        self.exp = GU.CalEnemyExp(self.hp)
        super().__init__()

        self.image = pygame.image.load(ENEMY_IMG_URL).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(self.rect.width, WIDTH - self.rect.width),-self.rect.height)
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        alpha = self.image.get_alpha()
        if alpha != 255: self.image.set_alpha(alpha+5)
        # if self.rect.top > HEIGHT:
        #     self.kill()
    
    def takenDamage(self,damage:int):
        self.hp -= damage
        self.image.set_alpha(180)
        # print(f"Hit me! My HP is {self.hp}")
    
    def isDead(self):
        return self.hp <= 0