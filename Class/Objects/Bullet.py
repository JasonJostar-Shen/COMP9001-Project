import pygame
import math
from Class.Objects.Enemy import Enemy
from Utils.Setting import WIDTH,HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self,damage,pos,target:Enemy,bounces,bounceRange):
        super().__init__()
        self.damage = damage
        self.image = pygame.Surface((5,5),pygame.SRCALPHA)
        pygame.draw.circle(self.image,(255,255,0),(4,4),4)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.target = target
        self.speed = 15
        dx = target.rect.center[0] - pos[0]
        dy = target.rect.center[1] - pos[1]
        distance = math.hypot(dx,dy)
        if distance == 0:
            distance = 1
        self.velocity = (dx/distance * self.speed, dy/distance * self.speed)
        self.bounces = bounces
        self.bounceRange = bounceRange
        self.attackedTargets = []
    
    def calVelocity(self):
        dx = self.target.rect.center[0] - self.rect.center[0]
        dy = self.target.rect.center[1] - self.rect.center[1]
        distance = math.hypot(dx,dy)
        if distance == 0:
            distance = 1
        self.velocity = (dx/distance * self.speed, dy/distance * self.speed)

    def update(self,isFast):
        if self.target.alive(): self.calVelocity()
        self.rect.x += self.velocity[0]*2 if isFast else self.velocity[0]
        self.rect.y += self.velocity[1]*2 if isFast else self.velocity[1]
        if (self.rect.right < 0 or self.rect.left > WIDTH
            or self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()
            
    def findNewTarget(self,enemies):
        closest = None
        min_distance = self.bounceRange
        for enemy in enemies:
            if enemy in self.attackedTargets or not enemy.alive():
                continue
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance < min_distance:
                min_distance = distance
                closest = enemy
        return closest
    
    def bounce(self,enemies):
        if self.bounces > 0:
            self.attackedTargets.append(self.target)
            self.target = self.findNewTarget(enemies)
            if self.target:
                self.bounces -= 1
                self.calVelocity()
                return True
        return False