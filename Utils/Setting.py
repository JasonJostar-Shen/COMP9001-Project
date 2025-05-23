BG_URL = "Assets/Images/bg.jpg"

FPS = 60
WIDTH, HEIGHT = 600, 750
STATUSWIDTH = 100

ENEMY_DICT = {
    'EyeLander':{
    'hp':100,
    'speed':0.5,
    'expParam':1,
    'url':'Assets/Images/EyeLander.png',
    'hpInterval':15,
    'hpIncrement':20,
    'speedInterval':250,
    'speedIncrement':0.25,
    'score':50
    },
    'Claw':{
    'hp':50,
    'speed':1,
    'expParam':1,
    'url':'Assets/Images/Claw.png',
    'hpInterval':15,
    'hpIncrement':20,
    'speedInterval':250,
    'speedIncrement':0.25,
    'score':100
    },
    'CasaMonstro':{
        'hp':2000,
        'speed':0.2,
        'expParam':1,
        'url':'Assets/Images/CasaMonstro.png',
        'hpInterval':75,
        'hpIncrement':100,
        'speedInterval':50,
        'speedIncrement':0,
        'score': 2000
    },
    'test':{
        'hp':5000,
        'speed':1,
        'expParam':1,
        'url':'Assets/Images/CasaMonstro.png',
        'hpInterval':100,
        'hpIncrement':100,
        'speedInterval':100,
        'speedIncrement':0.2,
        'score':2000
    }
    }
ENEMY_SPWAN_WEIGHT = [0.8,0.2,0,0]


ENEMY_COOLDOWN = 2500
ENEMY_COOLDOWN_MIN = 250
ENEMY_MAX_NUM = 5


PLAYER_INITHP = 2500
PLAYER_AS = 2000
PLAYER_DAMAGE = 50
PLAYER_LV_GAP = [100,100,150,200,300,350,1000]
PLAYER_LV_GAP_INTERVAL = 15
PLAYER_BASE_URL = 'Assets/Images/base.png'
PLAYER_TURRET_URL = 'Assets/Images/turret.png'
PLAYER_HP_SCORE = 2


SOUND_BGM_URL = "Assets/Sounds/background.mp3"
SOUND_FIRE_URL ="Assets/Sounds/fire.mp3"
SOUND_HIT_ENEMY_URL = "Assets/Sounds/hit1.mp3"
SOUND_HIT_PLAYER_URL = "Assets/Sounds/hit2.mp3"
SOUND_LVUP_URL = "Assets/Sounds/lvup.mp3"
SOUND_GAMEOVER_URL = "Assets/Sounds/gameover.mp3"
SOUND_WARNING_URL = "Assets/Sounds/warning.mp3"
SOUND_FINAL_URL = "Assets/Sounds/finalBattle.mp3"

WALL_URL = "Assets/Images/wall.png"
UPGRADE_DICT = {'ATK':[30,50,75,200],'Range':[50,75,100,200],'AS':[10,15,30,50],'HP':[25,50,75,100],'Bounce':1}
UPGRADE_WEIGHT_KEY = [0.4,0.1,0.4,0.08,0.02]
UPGRADE_WEIGHT_VALUE = [0.6,0.33,0.05,0.02]

EFFECT_TYPE = ['FadeOut','UpFadeOut']
