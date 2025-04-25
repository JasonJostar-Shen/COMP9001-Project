import pygame
from Class.Objects.Player import Player
from Class.Objects.Enemy import Enemy
from Class.Objects.Effect import Effect
from Class.Components.Wall import Wall
from Class.Components.StatusBar import StatusBar
from Class.Components.UpgradeWindow import UpgradeWindow
import Utils.GameUtils as GU
import Utils.Setting as config



def initWindow():
    bg = pygame.image.load(config.BG_URL).convert()
    bg = pygame.transform.scale(bg, (config.WIDTH, config.HEIGHT))
    return bg

def initSprites():
    player = Player()
    sprites = pygame.sprite.LayeredUpdates()
    enemySprites = pygame.sprite.LayeredUpdates()
    bulletsSprites = pygame.sprite.LayeredUpdates()
    effectSprites = pygame.sprite.LayeredUpdates()
    wall = Wall()
    # sprites.add(player,layer = 2)
    sprites.add(wall,layer = 1)
    statusBar = StatusBar(player)
    return player,wall,sprites,enemySprites,bulletsSprites,effectSprites,statusBar

def generateEnemy(sprites:pygame.sprite.LayeredUpdates,player:Player):
    enemyConfig = config.ENEMY_DICT['Eyeball']
    hp = GU.CalEnemyHP(player.kills,enemyConfig['hp'],enemyConfig['hpInterval'],enemyConfig['hpIncrement'])
    speed = GU.CalEnemyHP(player.kills,enemyConfig['speed'],enemyConfig['speedInterval'],enemyConfig['speedIncrement'])
    enemy = Enemy(hp,speed,enemyConfig['url'],enemyConfig['score'])
    # print(hp,speed)
    sprites.add(enemy,layer = 0)
    
def generateEffect(group:pygame.sprite.LayeredUpdates,type,pos,frame,text=None,fontSize=14,url=None):
    group.add(Effect(type,pos,frame,text,fontSize,url))

def collsionEvent(player:Player,wall,enemies,bullets,effects):
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
            text = f'-{player.atk}'
            textsize = 14
            pos = (enemy.rect.midtop[0],enemy.rect.midtop[1] - textsize//2)
            generateEffect(effects,'FadeOut',pos,45,text=text,fontSize=textsize)
            if enemy.isDead():
                player.gainExp(enemy.exp,enemy.score)
                generateEffect(effects,'FadeOut',enemy.rect.center,frame=30,url=config.ENEMY_IMG_URL)
                enemy.kill()
                
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH + config.STATUSWIDTH, config.HEIGHT))
        pygame.display.set_caption("DefendSpace")
        self.bg = initWindow()
        self.clock = pygame.time.Clock()
        self.isQuit = False
        self.restart()

    def restart(self):
        self.player, self.wall, self.sprites, self.enemySprites, self.bulletSprites, self.effectSprites, self.statusBar = initSprites()
        self.isPause = False
        self.upgradeWin = None
        self.startTime = pygame.time.get_ticks()
        self.enemyRespondTime = self.startTime
        self.playerFireTime = self.startTime
        self.pauseTime = None

    def run(self):
        while not self.isQuit:
            self.clock.tick(config.FPS)
            curTime = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isQuit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isQuit = True
                    elif event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_p and self.upgradeWin is None:
                        self.isPause = not self.isPause
                        if self.isPause:
                            self.pauseTime = curTime

                if self.upgradeWin is not None:
                    result = self.upgradeWin.handleEvent(event)
                    if result is not None:
                        self.player.lvUp(self.options[result])
                        self.upgradeWin = None
                        self.isPause = False

            if self.player.isUpgrade() and self.upgradeWin == None:
                self.isPause = True
                self.pauseTime = curTime
                self.options = GU.GenerateUpgradeOption(3)
                self.upgradeWin = UpgradeWindow(self.screen, self.options)

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
            enemyMax = GU.CalEnemyMax(self.player.kills)
            enemyCD = GU.CalEnemyCD(self.player.kills)

            if curEnemy < enemyMax and (curTime - self.enemyRespondTime) >= enemyCD:
                generateEnemy(self.enemySprites,self.player)
                self.enemyRespondTime = curTime

            if curTime - self.playerFireTime >= self.player.atkSpeed:
                self.playerFireTime = curTime
                self.player.shoot(self.bulletSprites)

            collsionEvent(self.player, self.wall, self.enemySprites, self.bulletSprites,self.effectSprites)
            self.player.findTarget(self.enemySprites)
            self.player.update()
            self.bulletSprites.update()
            self.enemySprites.update()
            self.effectSprites.update()

            self.screen.blit(self.bg, (0, 0))
            self.sprites.draw(self.screen)
            self.player.aimTarget(self.screen)
            self.bulletSprites.draw(self.screen)
            # self.enemySprites.draw(self.screen)
            for enemy in self.enemySprites:
                enemy.draw(self.screen)
            self.effectSprites.draw(self.screen)
            self.player.draw(self.screen)
            self.statusBar.update(self.screen)

            pygame.display.flip()

        pygame.quit()
    


if __name__ == '__main__':
    game = Game()
    game.run()
