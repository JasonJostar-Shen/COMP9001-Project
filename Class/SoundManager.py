import pygame
from Utils import Setting as config
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.fireSound = pygame.mixer.Sound(config.SOUND_FIRE_URL)
        self.hitEnemySound = pygame.mixer.Sound(config.SOUND_HIT_ENEMY_URL)
        self.hitPlayerSound = pygame.mixer.Sound(config.SOUND_HIT_PLAYER_URL)
        self.lvUpSound = pygame.mixer.Sound(config.SOUND_LVUP_URL)
        self.gameoverSound = pygame.mixer.Sound(config.SOUND_GAMEOVER_URL)
        self.warningSound = pygame.mixer.Sound(config.SOUND_WARNING_URL)
        pygame.mixer.music.load(config.SOUND_BGM_URL)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)
    
    def shoot(self):
        self.fireSound.set_volume(0.45)
        self.fireSound.stop()
        self.fireSound.play()
    
    def hitEnemy(self):
        self.hitEnemySound.set_volume(0.7)
        self.hitEnemySound.stop()
        self.hitEnemySound.play()
        
    def hitPlayer(self):
        self.hitPlayerSound.set_volume(1.2)
        self.hitPlayerSound.play()
    
    def lvUp(self):
        self.lvUpSound.set_volume(0.5)
        self.lvUpSound.play()
    
    def warning(self):
        self.lvUpSound.set_volume(0.8)
        self.warningSound.play()
    
    def gameOver(self):
        self.fireSound.stop()
        self.hitEnemySound.stop()
        self.hitPlayerSound.stop()
        pygame.mixer.music.stop()
        self.gameoverSound.set_volume(0.6)
        self.gameoverSound.play()
        
    def finalBattle(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(config.SOUND_FINAL_URL)
        pygame.mixer.music.play()