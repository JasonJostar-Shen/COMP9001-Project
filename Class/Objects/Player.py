import pygame
import math
import Utils.GameFormula as GF
from Class.Objects.Bullet import Bullet
from Utils.Setting import WIDTH,HEIGHT,PLAYER_INITHP,PLAYER_AS,PLAYER_DAMAGE,PLAYER_BASE_URL,PLAYER_TURRET_URL

INITPOSTION = (WIDTH // 2, HEIGHT-25)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.exp = 0
        self.hp = PLAYER_INITHP
        self.target = None
        self.angle = 0
        self.range = 500
        self.atk = PLAYER_DAMAGE
        self.attackSpeed = PLAYER_AS
        self.killcount = 0
        self.lv = 1
        super().__init__()
        self.baseImg = pygame.image.load(PLAYER_BASE_URL).convert_alpha()
        self.turretImg = pygame.image.load(PLAYER_TURRET_URL).convert_alpha()
        self.surface = pygame.Surface((50,50),pygame.SRCALPHA)
        # pygame.draw.polygon(self.surface, (0,255,0), [(25, 0), (0, 50), (50, 50)])
        # self.originalTurret = self.turretImg
        # self.originalBase = self.baseImg
        self.rect = self.surface.get_rect()
        self.rect.center = INITPOSTION
        # self.mask = pygame.mask.from_surface(self.surface)

    def draw(self,screen):
        self.rotatoToTarget()
        
        base = pygame.transform.rotate(self.baseImg,self.angle)
        baseRect = base.get_rect(center=self.rect.center)
        screen.blit(base,baseRect)
        
        turret = pygame.transform.rotate(self.turretImg,self.angle)

        offset = pygame.math.Vector2(0, -19)
        offset.rotate_ip(-self.angle)
        turretRect=turret.get_rect(center=self.rect.center+offset)
        screen.blit(turret,turretRect)
        

    def aimTarget(self,screen):
        if self.target:
            pygame.draw.line(screen, (255, 0, 0), self.rect.center, self.target.rect.center, 2)
    

    def gainExp(self,exp):
        self.exp += exp
        self.killcount += 1
        print(f"Player gained Exp!: {self.exp}")
            
    def isUpgrade(self):
        return self.exp >= GF.calLVGap(self.lv)

    def lvUp(self):
        self.exp -= GF.calLVGap(self.lv)
        self.lv += 1
        
    
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
            # rotated_image = pygame.transform.rotate(self.originalTurret, 0)
            self.angle = 0
            return

        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  # pygame y轴向下为正

        self.angle = angle - 90

        # rotated_image = pygame.transform.rotate(self.originalTurret, angle)

        # old_center = self.rect.center
        # self.surface = rotated_image
        # self.rect = self.surface.get_rect(center=old_center)

        

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