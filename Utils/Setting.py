BG_URL = "Assets/Images/bg.jpg"

FPS = 60
WIDTH, HEIGHT = 600, 900
STATUSWIDTH = 100

ENEMY_DICT = {
    'EyeLander':{
    'hp':100,
    'speed':0.75,
    'expParam':0.5,
    'url':'Assets/Images/EyeLander.png',
    'hpInterval':5,
    'hpIncrement':25,
    'speedInterval':100,
    'speedIncrement':0.5,
    'score':50
    },
    'Claw':{
    'hp':50,
    'speed':1.25,
    'expParam':1,
    'url':'Assets/Images/Claw.png',
    'hpInterval':10,
    'hpIncrement':25,
    'speedInterval':100,
    'speedIncrement':1,
    'score':100
    },
    'CasaMonstro':{
        'hp':1000,
        'speed':0.2,
        'expParam':1,
        'url':'Assets/Images/CasaMonstro.png',
        'hpInterval':50,
        'hpIncrement':1000,
        'speedInterval':100,
        'speedIncrement':0.2,
        'score':2000
    }
    }
ENEMY_SPWAN_WEIGHT = [0.8,0.2,0]
ENEMY_SCORE = 100
ENEMY_INITHP = 100
ENEMY_INITSPEED = 1
ENEMY_IMG_URL = 'Assets/Images/eyeball.png'


ENEMY_COOLDOWN = 2000
ENEMY_COOLDOWN_MIN = 500
ENEMY_MAX_NUM = 10


PLAYER_INITHP = 1000
PLAYER_AS = 2000
PLAYER_DAMAGE = 50
PLAYER_LV_GAP = [100,200,400,800,1000]
PLAYER_UPGRADE_AS = 20
PLAYER_UPGRADE_RANG = 50
PLAYER_UPGRADE_DAMAGE = 25
PLAYER_BASE_URL = 'Assets/Images/base.png'
PLAYER_TURRET_URL = 'Assets/Images/turret.png'
PLYAER_HP_SCORE = 2

UPGRADE_DICT = {'ATK':[10,25,50,100],'Range':[50,100,200],'AS':[10,15,20,50],'HP':[25,50,75,100],'Bounce':1}
UPGRADE_WEIGHT_KEY = [0.4,0.1,0.4,0.08,0.02]
UPGRADE_WEIGHT_VALUE = [0.6,0.33,0.05,0.02]

EFFECT_TYPE = ['FadeOut','UpFadeOut']
