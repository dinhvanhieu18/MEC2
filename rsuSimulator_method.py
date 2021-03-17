import random
import numpy as np
import math
from config import Config

def getAction(rsu, message, currentTime, network):

    # action = random.randint(0,2)
    # if action == 0:
    #     while True:
    #         neighbor = network.rsuList[random.randint(0, len(network.rsuList)-1)]
    #         if neighbor.id != rsu.id:
    #             break
    #     return (0, neighbor)
    # elif action == 1:
    #     return (1, network.gnb)
    # else:
    #     return (2, None)
    # 0: sendToRsu 
    stateInfo = rsu.optimizer.getState(message)
    rsu.optimizer.updateState(message)
    currentState = np.reshape(stateInfo[0], (1, len(stateInfo[0])))
    allActionValues = rsu.optimizer.onlineModel.predict(currentState)
    actionByPolicy = rsu.optimizer.policy(allActionValues)
    if actionByPolicy == 0:
        res = (0, stateInfo[1])
    elif actionByPolicy == 1:
        res = (1, network.gnb)
    else:
        res = (2, None)
    experience = [currentState, res[0], None, None]
    rsu.optimizer.addToMemoryTmp(experience, message)
    rsu.optimizer.update()
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

