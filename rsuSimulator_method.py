import random
import numpy as np
import math
from config import Config
from utils import calculateTaskInQueue

def getNeighborRsu(rsu):
    def sortFunc(e):
        return e[0] * e[1]
    tmp = []
    for rsu_ in rsu.neighbors:
        expectedTime = calculateTaskInQueue(rsu_) / Config.rsuProcessPerSecond
        tmp.append((expectedTime, rsu_.meanDelay, rsu_))
    tmp.sort(key=sortFunc)
    rand = random.random()
    if rand < 0.5:
        return tmp[0]
    else:
        return tmp[random.randint(0, len(tmp)-1)] 


def getState(rsu, message, network):
    # Info of this message
    res = [message.size, message.cpuCycle]
    # Info of this rsu
    # res.append(calculateTaskInQueue(rsu))
    res.append(rsu.meanDelayProcess)
    res.append(rsu.meanDelaySendToRsu)
    res.append(rsu.meanDelaySendToGnb)
    # Info of it's neighbor rsu
    neighborRsuInfo = getNeighborRsu(rsu)
    # res.append(neighborRsuInfo[0])
    res.append(neighborRsuInfo[1])
    # Info of gnb
    res.append(network.gnb.meanDelay)
    res = np.reshape(res, (1, len(res)))
    return (res, neighborRsuInfo[2])

def getAction(rsu, message, currentTime, network):
    # 1: rsu, 2: gnb, 3: process
    stateInfo = getState(rsu, message, network)
    currentState = stateInfo[0]
    neighborRsu = stateInfo[1]
    # Update state
    rsu.optimizer.updateState(message, currentState)
    # get values of all actions
    allActionValues = rsu.optimizer.onlineModel.predict(currentState)[0]
    # exclude actions can't choose
    exclude_actions = []
    if len(message.indexRsu) >= 2:
        exclude_actions.append(0)
    # get action by policy
    actionByPolicy = rsu.optimizer.policy(allActionValues, exclude_actions)
    experience = [currentState, actionByPolicy, None, None]
    rsu.optimizer.addToMemoryTmp(experience, message)
    rsu.optimizer.update()
    # return tuple of action and object the message will be in
    if actionByPolicy == 0:
        res = (1, neighborRsu)
    elif actionByPolicy == 1:
        res = (2, network.gnb)
    else:
        res = (3, None)
    return res

def distanceToCar(rsu, car, currentTime):
    positionCar = car.getPosition(currentTime)
    return math.sqrt(
        pow(positionCar - rsu.xcord, 2) + \
        pow(rsu.ycord, 2) + pow(rsu.zcord, 2))


def distanceToRsu(rsu, rsu_):
    return math.sqrt(
        pow(rsu.xcord - rsu_.xcord, 2) + \
        pow(rsu.ycord - rsu_.ycord, 2) + \
        pow(rsu.zcord - rsu_.zcord, 2)) 

