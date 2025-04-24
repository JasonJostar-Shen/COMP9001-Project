import pygame
import random
import Utils.GameFormula as GF
from Utils.Setting import WIDTH,HEIGHT,ENEMY_INITHP,ENEMY_INITSPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self,hp):
        self.hp = hp
        self.speed = ENEMY_INITSPEED
        self.exp = GF.calEnemyExp(self.hp)
        super().__init__()

        self.image = pygame.Surface((20,20),pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255,0,0), [(0, 0), (20, 0), (10, 20)])
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(self.rect.width, WIDTH - self.rect.width),-self.rect.height)
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        # if self.rect.top > HEIGHT:
        #     self.kill()
    
    def takenDamage(self,damage:int):
        self.hp -= damage
        print(f"Hit me! My HP is {self.hp}")
    
    def isDead(self):
        return self.hp <= 0