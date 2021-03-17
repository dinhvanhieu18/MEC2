import random
import numpy as np
import math
from config import Config

def getAction(car, message, currentTime, network):
    """Gat action of this car for the message

    Args:
        car ([CarSimulator]): [description]
        message ([Message]): [description]
        currentTime ([float]): [description]
        network ([Network]): [description]

    Returns:
        action: [0:sendToCar, 1:sendToRsu, 2:sendToGnb or 3:process]
        nextLocation: [The location where the message will be sent to]
    """    
    # 0: car, 1:rsu, 2:gnb, 3:process
    stateInfo = car.optimizer.getState(message)
    car.optimizer.updateState(message)
    currentState = np.reshape(stateInfo[0], (1, len(stateInfo[0])))
    allActionValues = car.optimizer.onlineModel.predict(currentState)
    actionByPolicy = car.optimizer.policy(allActionValues)
    if actionByPolicy == 0:
        if stateInfo[1]:
            res = (0, stateInfo[1])
        elif stateInfo[2]:
            res = (1, stateInfo[2])
        else:
            res = (2, network.gnb)
    elif actionByPolicy == 1:
        if stateInfo[2]:
            res = (1, stateInfo[2])
        else:
            res = (2, network.gnb)
    elif actionByPolicy == 2:
        res = (2, network.gnb)
    else:
        res = (3, None)
    experience = [currentState, res[0], None, None]
    car.optimizer.addToMemoryTmp(experience, message)
    car.optimizer.update()
    return res


def getPosition(car, currentTime):    
    return Config.carSpeed * (currentTime - car.startTime)

def distanceToCar(car1, car2, currentTime):
    return abs(car1.getPosition(currentTime) - car2.getPosition(currentTime))

def distanceToRsu(car, rsu, currentTime):
    position = car.getPosition(currentTime)
    return math.sqrt(
        pow(position - rsu.xcord, 2) + pow(rsu.ycord, 2) + pow(rsu.zcord, 2)
    )  

