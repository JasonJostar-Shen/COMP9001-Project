import pygame
from Utils import Setting as config
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.fireSound = pygame.mixer.Sound(config.SOUND_FIRE_URL)
        self.hitEnemySound = pygame.mixer.Sound(config.SOUND_HIT_ENEMY_ULR)
        self.hitPlayerSound = pygame.mixer.Sound(config.SOUND_HIT_ENEMY_ULR)
        pygame.mixer.music.load(config.SOUND_BGM_URL)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)
    
    def shoot(self):
        self.fireSound.set_volume(0.7)
        self.fireSound.play()
    
    def hitEnemy(self):
        self.hitEnemySound.set_volume(0.6)
        self.hitEnemySound.play()
        
    def hitPlayer(self):
        self.hitPlayerSound.set_volume(0.6)
        self.hitPlayerSound.play()