import pygame
from Class.Objects.Player import Player
from Class.Objects.Enemy import Enemy
from Class.Components.Wall import Wall
from Class.Components.StatusBar import StatusBar
from Utils.Setting import WIDTH,HEIGTH,ENEMY_MAX,ENEMY_COOLDOWN,FPS,BG_URL,STATUSWIDTH

def initWindow():
    bg = pygame.image.load(BG_URL).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGTH))
    return bg

def initSprites():
    player = Player()
    sprites = pygame.sprite.LayeredUpdates()
    enemySprites = pygame.sprite.LayeredUpdates()
    bulletsSprites = pygame.sprite.LayeredUpdates()
    wall = Wall()
    sprites.add(player,layer = 2)
    sprites.add(wall,layer = 1)
    statusBar = StatusBar(player)
    return player,wall,sprites,enemySprites,bulletsSprites,statusBar

def generateEnemy(sprites:pygame.sprite.LayeredUpdates):
    enemy = Enemy()
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
            enemy.takenDamage(player.damage)
            if enemy.isDead():
                player.gainExp(enemy.exp)
                enemy.kill()
                
            # for enemy in bulletHitEnenmy:
            #     print("Hit!")


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH+STATUSWIDTH,HEIGTH))
    pygame.display.set_caption("TestWindow")
    bg = initWindow()
    isPause = False
    player,wall,sprites,enemySprites,bulletSprites,statusBar = initSprites()
    clock = pygame.time.Clock()
    isEnd = False
    startTime = pygame.time.get_ticks()
    enemyRespondTime = startTime
    playerFireTime = startTime
    pauseTime = None
    while not isEnd:
        clock.tick(FPS)
        curTime = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isEnd = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isEnd = True
                if event.key == pygame.K_p:
                    isPause = not isPause
                    if isPause:
                        pauseTime = curTime
                        
        if isPause: continue
        if pauseTime != None:
            deltaTime = curTime - pauseTime
            enemyRespondTime += deltaTime
            playerFireTime += deltaTime
            pauseTime = None
        curEnemy = len(enemySprites)
        # print(curTime,enemyRespondtime)
        if curEnemy < ENEMY_MAX and (curTime - enemyRespondTime) >= ENEMY_COOLDOWN:
            generateEnemy(enemySprites)
            curEnemy = len(enemySprites)
            enemyRespondTime = curTime
            print(f"EnemyNum: {curEnemy}")  
        if curTime - playerFireTime >= player.fireSpeed:
            playerFireTime = curTime
            player.shoot(bulletSprites)
        collsionEvent(player,wall,enemySprites,bulletSprites)

        player.findTarget(enemySprites)
        player.update()
        bulletSprites.update()
        enemySprites.update()

        screen.blit(bg, (0,0))
        player.aimTarget(screen)
        sprites.draw(screen)
        bulletSprites.draw(screen)
        enemySprites.draw(screen)
        statusBar.update(screen)
        if player.isUpgrade():
            isPause = True
            pauseTime = curTime
            player.lvUp()

        pygame.display.flip()
        

    pygame.quit()