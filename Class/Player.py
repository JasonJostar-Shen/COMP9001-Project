import pygame
import math
import Utils.GameFormula as GF
from Class.Bullet import Bullet
# from Bullet import Bullet
from Utils.Setting import WIDTH,HEIGTH,PLAYER_INITHP,PLAYER_FIRESPEED,PLAYER_DAMAGE,STATUSWIDTH

INITPOSTION = (WIDTH // 2, HEIGTH-50)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.exp = 0
        self.hp = PLAYER_INITHP
        self.target = None
        self.angle = 0
        self.range = 500
        self.damage = PLAYER_DAMAGE
        self.fireSpeed = PLAYER_FIRESPEED
        self.lv = 1
        super().__init__()
        self.image = pygame.Surface((50,50),pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0,255,0), [(25, 0), (0, 50), (50, 50)])
        self.originalImage = self.image
        self.rect = self.image.get_rect()
        self.rect.center = INITPOSTION
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rotatoToTarget()

    def aimTarget(self,screen):
        if self.target:
            pygame.draw.line(screen, (255, 0, 0), self.rect.center, self.target.rect.center, 2)

    def gainExp(self,exp):
        self.exp += exp
        print(f"Player gained Exp!: {self.exp}")
        lvGap = GF.calLVGap(self.lv)
        if self.exp > lvGap:
            self.exp -= lvGap
            self.lv += 1
            print(f"Level Up! I am LV{self.lv} now! Exp is {self.exp}")

    def findTarget(self,group):
        if len(group) == 0: return
        target = None
        minDistance = self.range
        for enemy in group:
            dx = self.rect.centerx - enemy.rect.centerx
            dy = self.rect.centery - enemy.rect.centery
            distance = math.hypot(dx,dy)
            # print(distance)
            if distance < minDistance:
                minDistance = distance
                target = enemy
        if minDistance == self.range: target == None
        self.target = target


    def rotatoToTarget(self):
        if self.target is None:
            rotated_image = pygame.transform.rotate(self.originalImage, 0)
            self.angle = 0
            return

        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  # pygame y轴向下为正

        corrected_angle = angle - 90

        rotated_image = pygame.transform.rotate(self.originalImage, corrected_angle)

        old_center = self.rect.center
        self.image = rotated_image
        self.rect = self.image.get_rect(center=old_center)

        self.angle = corrected_angle

    def takenDamage(self,damage:int):
        self.hp -= damage
        print(f"Hurt! Hp:{self.hp}")
    
    def shoot(self,bulletGroup):
        if self.target:
            bullet = Bullet(self.rect.center,self.target)
            bulletGroup.add(bullet)
    
    def hasTarget(self):
        return self.target != None
    
    def getLvGap(self):
        return GF.calLVGap(self.lv)