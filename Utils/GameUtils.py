import Utils.Setting as config
import random

def CalLVGap(curLV):
    interval = config.PLAYER_LV_GAP_INTERVAL
    gapLv = (curLV-1)//interval
    if gapLv == 0: return curLV * config.PLAYER_LV_GAP[0]
    gapLv = gapLv if gapLv < len(config.PLAYER_LV_GAP) else len(config.PLAYER_LV_GAP) - 1
    lastExpGap = 0
    for i in range(gapLv):
        if gapLv > i:
            lastExpGap += config.PLAYER_LV_GAP[i] * interval
    lastExpGap += config.PLAYER_LV_GAP[gapLv] * (curLV - gapLv * interval)
    return lastExpGap

def CalEnemyExp(score,expParam):
    return score * expParam

def CalEnemyHP(curKills,hp,interval,increment):
    hp = hp  * ((1 + (increment / 100)) **(curKills // interval))
    return int(hp)

def CalEnemySpeed(curKills,speed,interval,increment):
    return speed + curKills // interval * increment

def CalEnemyCD(curKills):
    cd = config.ENEMY_COOLDOWN - curKills//10 * 100
    cd =  cd if cd > config.ENEMY_COOLDOWN_MIN else config.ENEMY_COOLDOWN_MIN
    return cd
    
def CalEnemyMax(curKills):
    return config.ENEMY_MAX_NUM + curKills//10

def GenerateUpgradeOption(num):
    upgradeDict = config.UPGRADE_DICT
    options = []
    for i in range(num):
        key = random.choices(list(upgradeDict.keys()),weights=config.UPGRADE_WEIGHT_KEY,k=1)[0]
        if key == 'Bounce':
            value = 1
            index = 3
        else:
            valueList = upgradeDict[key]
            value = random.choices(valueList,weights=config.UPGRADE_WEIGHT_VALUE,k=1)[0]
            index = valueList.index(value)
        options.append((key,value,index))
    return options

def GenerateEnemyConfig():
    enemyDict = config.ENEMY_DICT
    key = random.choices(list(enemyDict.keys()),weights=config.ENEMY_SPWAN_WEIGHT,k=1)[0]
    return enemyDict[key]

def GetOptionText(option):
    attribute = option[0]
    value = option[1]
    if  attribute == 'Range' or attribute == 'Bounce':
        return f'{attribute} +{value}'
    if attribute == 'AS':
        return f'{attribute} -{value}%'
    if attribute == 'HP' or attribute == 'ATK':
        return f'{attribute} +{value}%'
    
# def CalPlayerHp(curLv):
#     return int(config.PLAYER_INITHP * (1+config.PLAYER_HP_INCREMENT/100) ** ((curLv - 1) // config.PLAYER_HP_INTERVAL))
    