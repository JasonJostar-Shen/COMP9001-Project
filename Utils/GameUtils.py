import Utils.Setting as config
import random

def CalLVGap(curLV):
    gapLv = (curLV - 1) // 3
    if gapLv == 0: return curLV * config.PLAYER_LV_GAP[0]
    gapLv = gapLv if gapLv < 4 else 4
    lastExpGap = 0
    for i in range(gapLv):
        if gapLv > i:
            lastExpGap += config.PLAYER_LV_GAP[i] * 3
        else:
            lastExpGap += config.PLAYER_LV_GAP[i] * (curLV - gapLv*3)
    return lastExpGap

def CalEnemyExp(initHP):
    return int(initHP*config.ENEMY_EXP_PARAM)

def CalEnemyHP(curKills):
    return config.ENEMY_INITHP + curKills // 5 * 25

def CalEnemySpeed(curKills):
    return config.ENEMY_INITSPEED + curKills // 80 * 1

def CalEnemyCD(curKills):
    cd = config.ENEMY_COOLDOWN - curKills//10 * 100
    cd =  cd if cd > config.ENEMY_COOLDOWN_MIN else config.ENEMY_COOLDOWN_MIN
    return cd
    
def CalEnemyMax(curKills):
    return config.ENEMY_MAX + curKills//10

def GenerateUpgradeOption(num):
    upgradeDict = config.UPGRADE_DICT
    options = []
    for i in range(num):
        key = random.choices(list(upgradeDict.keys()),weights=config.UPGRADE_WEIGHT_KEY,k=1)[0]
        valueList = upgradeDict[key]
        value = random.choices(valueList,weights=config.UPGRADE_WEIGHT_VALUE,k=1)[0]
        index = valueList.index(value)
        options.append((key,value,index))
    return options

def GetOptionText(option):
    attribute = option[0]
    value = option[1]
    if attribute == 'ATK' or attribute == 'Range':
        return f'{attribute} +{value}'
    if attribute == 'AS':
        return f'{attribute} -{value}%'
    