import pygame
from Class.Objects.Player import Player
from Class.Objects.Enemy import Enemy
from Class.Objects.Effect import Effect
from Class.Components.Wall import Wall
from Class.Components.StatusBar import StatusBar
from Class.Components.UpgradeWindow import UpgradeWindow
from Class.SoundManager import SoundManager
import Utils.GameUtils as GU
import Utils.Setting as config



def initWindow():
    bg = pygame.image.load(config.BG_URL).convert()
    bg = pygame.transform.scale(bg, (config.WIDTH, config.HEIGHT))
    return bg



def generateEnemy(sprites:pygame.sprite.LayeredUpdates,player:Player,enemyConfig):
    hp = GU.CalEnemyHP(player.kills,enemyConfig['hp'],enemyConfig['hpInterval'],enemyConfig['hpIncrement'])
    speed = GU.CalEnemySpeed(player.kills,enemyConfig['speed'],enemyConfig['speedInterval'],enemyConfig['speedIncrement'])
    enemy = Enemy(hp,speed,enemyConfig['url'],enemyConfig['score'],enemyConfig['expParam'])
    sprites.add(enemy,layer = 0)
    
def generateEffect(group:pygame.sprite.LayeredUpdates,type,pos,frame,text=None,fontSize=14,fontColor=(255,255,255),url=None):
    group.add(Effect(type,pos,frame,text,fontSize,fontColor,url))


                
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH + config.STATUSWIDTH, config.HEIGHT),pygame.SCALED)
        # self.screen = pygame.display.set_mode((config.WIDTH + config.STATUSWIDTH, config.HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption("DefendSpace")
        self.bg = initWindow()
        self.clock = pygame.time.Clock()
        self.isQuit = False
        self.isOver = False
        self.isFinal = False
        self.isFullScreen = False
        self.restart()

    def restart(self):
        self.player, self.wall, self.sprites, self.enemySprites, self.bulletSprites, self.effectSprites, self.statusBar = self.initSprites()
        self.SoundMananger = SoundManager()
        self.isPause = False
        self.isFast = False
        self.isOver = False
        self.isFinal = False
        self.upgradeWin = None
        self.startTime = pygame.time.get_ticks()
        self.enemyRespondTime = self.startTime
        self.playerFireTime = self.startTime
        self.pauseTime = None

    def initSprites(self):  
        player = Player()
        sprites = pygame.sprite.LayeredUpdates()
        enemySprites = pygame.sprite.LayeredUpdates()
        bulletsSprites = pygame.sprite.LayeredUpdates()
        effectSprites = pygame.sprite.LayeredUpdates()
        wall = Wall()
        sprites.add(wall, layer=1)
        statusBar = StatusBar(
            player,
            onPause=self.togglePasue,
            onFast=self.toggleFast,
            onRestart=self.restart,
            onQuit=self.quitGame
        )
        return player, wall, sprites, enemySprites, bulletsSprites, effectSprites, statusBar
    
    def collsionEvent(self,player:Player,wall,enemies,bullets,effects):
        EnenmyHitWall = pygame.sprite.spritecollide(wall,enemies, dokill=True)
        if EnenmyHitWall:
            for enemy in EnenmyHitWall:
                player.takenDamage(enemy.exp)
                self.SoundMananger.hitPlayer()
                generateEffect(effects,'UpFadeOut', player.rect.midtop,30,text=f'-{enemy.exp}',fontSize=20,fontColor=(200,100,100))
        
        for enemy in enemies:
            bulletHitEnenmy = pygame.sprite.spritecollide(enemy,bullets, dokill=False)
            if bulletHitEnenmy:
                
                for bullet in bulletHitEnenmy:
                    if enemy not in bullet.attackedTargets:
                        enemy.takenDamage(bullet.damage)
                        self.SoundMananger.hitEnemy()
                        text = f'-{player.atk}'
                        textsize = 14
                        pos = (enemy.rect.midtop[0],enemy.rect.midtop[1] - textsize//2)
                        generateEffect(effects,'FadeOut',pos,45,text=text,fontSize=textsize)
                        if not bullet.bounce(enemies):
                            bullet.kill()
                
                if enemy.isDead():
                    player.gainExp(enemy.exp,enemy.score)
                    if player.kills % 50 == 0:
                        generateEnemy(enemies,player,config.ENEMY_DICT['CasaMonstro'])
                    if player.kills == 1000:
                        self.isFinal = True
                        self.SoundMananger.finalBattle()
                        for i in range(9):
                            generateEnemy(enemies,player,config.ENEMY_DICT['CasaMonstro'])
                    generateEffect(effects,'FadeOut',enemy.rect.center,frame=30,url=enemy.url)
                    enemy.kill()
    
    def gameOver(self):
        overlay = pygame.Surface(self.screen.get_size(),pygame.SRCALPHA)
        overlay.fill((0,0,0))
        overlay.set_alpha(180)
        font = pygame.font.SysFont('arial',48)
        title = font.render("GAME OVER!",True,(255,255,255))
        titleRect = title.get_rect()
        font = pygame.font.SysFont('arial',32)
        score = self.player.score if self.player.hp <= 0 else self.player.score + self.player.hp * config.PLAYER_HP_SCORE
        texts = [font.render(f"Your Score is {score}",True,(255,255,255)),
                 font.render("Press'R' to Restart!",True,(255,255,255))]
        titleRect.center = (self.screen.get_width()//2,self.screen.get_height()//3)
        self.screen.blit(self.screenShot,(0,0))
        self.screen.blit(overlay,(0,0))
        self.screen.blit(title,titleRect)
        for i, text in enumerate(texts):
            textRect = text.get_rect()
            textRect.center = (self.screen.get_width()//2, self.screen.get_height()//2 + i * 50)
            self.screen.blit(text,textRect)
        pygame.display.flip()
    
    def togglePasue(self):
        self.isPause = not self.isPause
        if self.isPause:
            self.pauseTime = self.curTime
    
    def toggleFast(self):
        self.isFast = not self.isFast
        
    def quitGame(self):
        self.isQuit = True
    
    def checkOver(self):
        if not self.player.isAlive():
            return True
        if self.isFinal:
            aliveEnemies = [enemy for enemy in self.enemySprites if enemy.alive()]
            aliveCount = len(aliveEnemies)
            if aliveCount == 0: return True
        return False
    
    def run(self):
        while not self.isQuit:
            self.clock.tick(config.FPS)
            self.curTime = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isQuit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quitGame()
                    elif event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_p and self.upgradeWin is None:
                        # self.isPause = not self.isPause
                        # if self.isPause:
                        #     self.pauseTime = self.curTime
                        self.togglePasue()
                        self.statusBar.buttons[0].selected  = self.isPause
                        
                    elif event.key == pygame.K_f:
                        self.toggleFast()
                        self.statusBar.buttons[1].selected = self.isFast
                    elif event.key == pygame.K_c:
                        self.isOver = True
                        self.screenShot = self.screen.copy()
                        self.SoundMananger.gameOver()
                        continue
                    elif event.key == pygame.K_F5:
                        print(self.screen.get_size())
                        print()
                        print(pygame.display.Info())
                        # self.player.bounce += 2
                        # self.player.range = 1000
                        # self.player.atk += 999999
                        # self.player.atkSpeed = 100
                    # elif event.key == pygame.K_F6:
                    #     generateEnemy(self.enemySprites,self.player,config.ENEMY_DICT['test'])
                    # elif event.key == pygame.K_F11:
                    #     self.isFullScreen = not self.isFullScreen
                    #     if self.isFullScreen:
                    #         self.screen = pygame.display.set_mode((config.WIDTH + config.STATUSWIDTH, config.HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
                    #     else:
                    #         self.screen.set

                if self.upgradeWin is not None:
                    result = self.upgradeWin.handleEvent(event)
                    if result is not None:
                        self.player.lvUp(result)
                        self.upgradeWin = None
                        self.isPause = False

            if self.player.isUpgrade() and self.upgradeWin == None:
                self.isPause = True
                self.pauseTime = self.curTime
                self.options = GU.GenerateUpgradeOption(3)
                self.upgradeWin = UpgradeWindow(self.screen, self.options)
                self.SoundMananger.lvUp()
                
            
            if self.isOver:
                self.gameOver()
                continue
            
            if self.isPause:
                self.statusBar.update(self.screen,pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
                if self.upgradeWin is not None:
                    self.upgradeWin.draw()
                else:
                    pygame.display.flip()
                continue

            if self.pauseTime is not None:
                deltaTime = self.curTime - self.pauseTime
                self.enemyRespondTime += deltaTime
                self.playerFireTime += deltaTime
                self.pauseTime = None

            
            
            if not self.isPause:
                if not self.isFinal:
                    curEnemy = len(self.enemySprites)
                    enemyMax = GU.CalEnemyMax(self.player.kills)
                    enemyCD = GU.CalEnemyCD(self.player.kills) // 2 if self.isFast else GU.CalEnemyCD(self.player.kills)

                    if curEnemy < enemyMax and (self.curTime - self.enemyRespondTime) >= enemyCD:
                        enemyConfig = GU.GenerateEnemyConfig()
                        generateEnemy(self.enemySprites,self.player,enemyConfig)
                        self.enemyRespondTime = self.curTime

                atkSpeed = self.player.atkSpeed // 2 if self.isFast else self.player.atkSpeed
                if self.curTime - self.playerFireTime >= atkSpeed:
                    self.playerFireTime = self.curTime
                    self.player.shoot(self.bulletSprites,self.SoundMananger)
                    

                self.collsionEvent(self.player, self.wall, self.enemySprites, self.bulletSprites,self.effectSprites)
                self.player.findTarget(self.enemySprites)
                self.player.update()
                self.bulletSprites.update(self.isFast)
                self.enemySprites.update(self.isFast)
                self.effectSprites.update()
            
            self.screen.fill((0,0,0))
            self.screen.blit(self.bg, (0, 0))
            self.sprites.draw(self.screen)
            # self.player.aimTarget(self.screen)
            self.bulletSprites.draw(self.screen)
                    
            for enemy in self.enemySprites:
                enemy.draw(self.screen)
            self.effectSprites.draw(self.screen)
            self.player.draw(self.screen)
            self.statusBar.update(self.screen,pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
            if self.upgradeWin is not None: 
                    self.upgradeWin.draw()
            self.isOver = self.checkOver()
            if self.isOver:
                self.SoundMananger.gameOver() 
                self.screenShot = self.screen.copy()
                
            pygame.display.flip()

        pygame.quit()
    


if __name__ == '__main__':
    game = Game()
    game.run()
