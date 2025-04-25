import pygame
import math
import Utils.GameUtils as GU
from Class.Objects.Bullet import Bullet
from Class.Components.ProgressBar import ProgressBar
from Utils.Setting import WIDTH,HEIGHT,PLAYER_INITHP,PLAYER_AS,PLAYER_DAMAGE,PLAYER_BASE_URL,PLAYER_TURRET_URL

INITPOSTION = (WIDTH // 2, HEIGHT-70)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.exp = 0
        self.maxHp = PLAYER_INITHP
        self.hp = PLAYER_INITHP
        self.target = None
        self.angle = 0
        self.range = 500
        self.atk = PLAYER_DAMAGE
        self.atkSpeed = PLAYER_AS
        self.kills = 0
        self.score = 0
        self.lv = 1
        super().__init__()
        self.baseImg = pygame.image.load(PLAYER_BASE_URL).convert_alpha()
        self.turretImg = pygame.image.load(PLAYER_TURRET_URL).convert_alpha()
        self.surface = pygame.Surface((50,50),pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.center = INITPOSTION
        self.lifeBar = ProgressBar(WIDTH,20,(WIDTH/2,HEIGHT-30),self.maxHp,30,title="HP")
        self.expBar = ProgressBar(WIDTH,20,(WIDTH/2,HEIGHT-10),self.getLvGap(),30,False,title="EXP"
                                  ,fillColor=(100, 150, 230),bgColor=(211, 211, 211))

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
        self.lifeBar.draw(screen)
        self.expBar.draw(screen)

    def aimTarget(self, screen):
        if self.target:
            surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            pygame.draw.line(surface, (255, 0, 0, 128), self.rect.center, self.target.rect.center, 2)
            screen.blit(surface, (0, 0))
    

    def gainExp(self,exp,score):
        self.exp += exp
        self.kills += 1
        self.score += score
        print(f"Player gained Exp!: {self.exp}")
            
    def isUpgrade(self):
        return self.exp >= GU.CalLVGap(self.lv)

    def lvUp(self,option):
        self.exp -= GU.CalLVGap(self.lv)
        self.lv += 1
        self.expBar.maxValue = self.getLvGap()
        self.expBar.setValue(self.exp)
        attribute = option[0]
        value = option[1]
        if attribute == 'AS':
            self.atkSpeed *= 1-value/100.0
        elif attribute == 'ATK':
            self.atk += value
        elif attribute == 'Range':
            self.range += value
        elif attribute == 'HP':
            self.hp += self.maxHp * value/100
            self.hp = self.hp if self.hp < self.maxHp else self.maxHp
        
    
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
            # self.angle = 0
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
        return GU.CalLVGap(self.lv)
    
    def update(self):
        self.lifeBar.update(self.hp)
        self.expBar.update(self.exp)
    