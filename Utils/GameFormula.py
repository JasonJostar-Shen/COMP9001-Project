import Utils.Setting as config
import math
def calLVGap(curLV):
    return curLV * config.PLAYER_LV_GAP

def calEnemyExp(initHP):
    return int(initHP*config.ENEMY_EXP_PARAM)