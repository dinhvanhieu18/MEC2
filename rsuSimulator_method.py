import random
import numpy as np
import math
import copy
from config import Config
from utils import calculateTaskInQueue
from utils import getLogger
logger = getLogger()

# def getNeighborRsuInfo(rsu):
#     def sortFunc(e):
#         return e[1]
#     tmp = []
#     for rsu_ in rsu.neighbors:
#         expectedTime = calculateTaskInQueue(rsu_) / Config.rsuProcessPerSecond
#         tmp.append((expectedTime, rsu_.meanDelay, rsu_))
#     tmp.sort(key=sortFunc)
#     rand = random.random()
#     if rand < 0.5:
#         return tmp[0]
#     else:
#         return tmp[random.randint(0, len(tmp)-1)] 


def getState(rsu, message, network):
    # Info of this message
    # res = [message.size, message.cpuCycle]
    # Info of this rsu
    # res.append(calculateTaskInQueue(rsu))
    res = []
    res.append(rsu.meanDelayProcess)
    # res.append(rsu.meanDelaySendToRsu)
    res.append(rsu.meanDelaySendToGnb)
    # Info of it's neighbor rsu
    # neighborRsuInfo = getNeighborRsuInfo(rsu)
    # res.append(neighborRsuInfo[0])
    # res.append(neighborRsuInfo[1])
    # Info of gnb
    res.append(network.gnb.meanDelay)
    res = np.reshape(res, (1, len(res)))
    return res

def getAction(rsu, message, currentTime, network):
    # 0: gnb, 1: process
    logger.info("Rsu {} get action with message stt {}".format(rsu.id, message.stt))
    if rsu.optimizer is not None:
        currentState = getState(rsu, message, network)
        rsu.optimizer.updateState(message, currentState)
        # get values of all actions
        allActionValues = rsu.optimizer.getAllActionValues(currentState)
        logger.info("All action values {}".format(allActionValues))
        # get action by policy
        actionByPolicy = car.optimizer.policy(allActionValues)
        logger.info("Choose action {}".format(actionByPolicy))
        # Update memory
        rsu.optimizer.addToMemoryTmp(message, currentState, actionByPolicy)
    else:
        rand = random.random()
        if rand < Config.default_pr:
            actionByPolicy = 0
        else:
            actionByPolicy = 1
    # return tuple of action and object the message will be in
    if actionByPolicy == 0:
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

