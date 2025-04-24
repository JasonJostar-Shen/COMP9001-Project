import pygame
from Class.Objects.Player import Player
from Class.Objects.Enemy import Enemy
from Class.Components.Wall import Wall
from Class.Components.StatusBar import StatusBar
from Class.Components.UpgradeWindow import UpgradeWindow
import Utils.GameUtils as GF
import Utils.Setting as config
from Utils.Setting import WIDTH,HEIGHT,FPS,BG_URL,STATUSWIDTH


def initWindow():
    bg = pygame.image.load(BG_URL).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    return bg

def initSprites():
    player = Player()
    sprites = pygame.sprite.LayeredUpdates()
    enemySprites = pygame.sprite.LayeredUpdates()
    bulletsSprites = pygame.sprite.LayeredUpdates()
    wall = Wall()
    # sprites.add(player,layer = 2)
    sprites.add(wall,layer = 1)
    statusBar = StatusBar(player)
    return player,wall,sprites,enemySprites,bulletsSprites,statusBar

def generateEnemy(sprites:pygame.sprite.LayeredUpdates,player:Player):
    hp = GF.calEnemyHP(player.kills)
    speed = GF.calEnemySpeed(player.kills)
    enemy = Enemy(hp,speed)
    # print(hp,speed)
    sprites.add(enemy,layer = 0)

def collsionEvent(player:Player,wall,enemies,bullets):
    EnenmyHitWall = pygame.sprite.spritecollide(wall,enemies, dokill=True)
    if EnenmyHitWall:
        for enemy in EnenmyHitWall:
            player.takenDamage(enemy.hp)
            for bullet in bullets:
                if bullet.target == enemy:
                    bullet.kill()
    
    for enemy in enemies:
        bulletHitEnenmy = pygame.sprite.spritecollide(enemy,bullets, dokill=True)
        if bulletHitEnenmy:
            enemy.takenDamage(player.atk)
            if enemy.isDead():
                player.gainExp(enemy.exp)
                enemy.kill()
                
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH + STATUSWIDTH, HEIGHT))
        pygame.display.set_caption("DefendSpace")
        self.bg = initWindow()
        self.clock = pygame.time.Clock()
        self.isEnd = False
        self.restart()

    def restart(self):
        self.player, self.wall, self.sprites, self.enemySprites, self.bulletSprites, self.statusBar = initSprites()
        self.isPause = False
        self.upgradeWin = None
        self.startTime = pygame.time.get_ticks()
        self.enemyRespondTime = self.startTime
        self.playerFireTime = self.startTime
        self.pauseTime = None

    def run(self):
        while not self.isEnd:
            self.clock.tick(FPS)
            curTime = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isEnd = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isEnd = True
                    elif event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_p and self.upgradeWin is None:
                        self.isPause = not self.isPause
                        if self.isPause:
                            self.pauseTime = curTime

                if self.upgradeWin is not None:
                    result = self.upgradeWin.handleEvent(event)
                    if result is not None:
                        self.upgradeWin = None
                        self.isPause = False
                        if result == 0:
                            self.player.attackSpeed *= 1 - (config.PLAYER_UPGRADE_AS / 100)
                        elif result == 1:
                            self.player.range += config.PLAYER_UPGRADE_RANG
                        elif result == 2:
                            self.player.atk += config.PLAYER_UPGRADE_DAMAGE

            if self.player.isUpgrade():
                self.isPause = True
                self.pauseTime = curTime
                self.player.lvUp()
                options = [f'AS +{config.PLAYER_UPGRADE_AS}%', f'Range +{config.PLAYER_UPGRADE_RANG}', f'ATK +{config.PLAYER_UPGRADE_DAMAGE}']
                self.upgradeWin = UpgradeWindow(self.screen, options)

            if self.isPause:
                if self.upgradeWin is not None:
                    self.upgradeWin.draw()
                continue

            if self.pauseTime is not None:
                deltaTime = curTime - self.pauseTime
                self.enemyRespondTime += deltaTime
                self.playerFireTime += deltaTime
                self.pauseTime = None

            curEnemy = len(self.enemySprites)
            enemyMax = GF.calEnemyMax(self.player.kills)
            enemyCD = GF.calEnemyCD(self.player.kills)

            if curEnemy < enemyMax and (curTime - self.enemyRespondTime) >= enemyCD:
                generateEnemy(self.enemySprites,self.player)
                self.enemyRespondTime = curTime

            if curTime - self.playerFireTime >= self.player.attackSpeed:
                self.playerFireTime = curTime
                self.player.shoot(self.bulletSprites)

            collsionEvent(self.player, self.wall, self.enemySprites, self.bulletSprites)
            self.player.findTarget(self.enemySprites)

            self.bulletSprites.update()
            self.enemySprites.update()

            self.screen.blit(self.bg, (0, 0))
            self.player.aimTarget(self.screen)
            self.sprites.draw(self.screen)
            self.bulletSprites.draw(self.screen)
            self.enemySprites.draw(self.screen)
            self.player.draw(self.screen)
            self.statusBar.update(self.screen)

            pygame.display.flip()

        pygame.quit()
    


if __name__ == '__main__':
    game = Game()
    game.run()
