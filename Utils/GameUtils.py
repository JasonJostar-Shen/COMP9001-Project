import Utils.Setting as config
import math
def calLVGap(curLV):
    return curLV * config.PLAYER_LV_GAP

def calEnemyExp(initHP):
    return int(initHP*config.ENEMY_EXP_PARAM)

def calEnemyHP(curKills):
    return config.ENEMY_INITHP + curKills // 5 * 10

def calEnemySpeed(curKills):
    return config.ENEMY_INITSPEED + curKills // 100 * 1

def calEnemyCD(curKills):
    cd = config.ENEMY_COOLDOWN - curKills//2 * 10
    cd =  cd if cd > config.ENEMY_COOLDOWN_MIN else config.ENEMY_COOLDOWN_MIN
    return cd
    
def calEnemyMax(curKills):
    return config.ENEMY_MAX + curKills//10