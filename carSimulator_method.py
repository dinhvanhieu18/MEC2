import random
import numpy as np
import math
import os
from config import Config
from utils import getNext
from message import Message
from utils import logger

def generateMessage(car, currentTime):
    numMessagePerSecond = int(car.packageStrategy.split("_")[-1])
    res = []
    preTime = currentTime
    while True:
        nextTime = preTime + getNext(numMessagePerSecond)
        if nextTime > currentTime + Config.cycleTime:
            return res
        else:
            mes = Message(indexCar=car.id, time=nextTime)
            res.append(mes)
            preTime = nextTime

# def getNeighborCarInfo(car):
#     def sortFunc(e):
#         return e[1]
#     tmp = []
#     for car_ in car.neighborCars:
#         expectedTime = calculateTaskInQueue(car_) / Config.carProcessPerSecond
#         tmp.append((expectedTime, car_.meanDelay, car_))
#     tmp.sort(key=sortFunc)
#     if not tmp:
#         # print("Don't has neighbor car")
#         return (0.0, 0.0, None)
#     rand = random.random()
#     if rand < 0.5:
#         return tmp[0]
#     else:
#         return tmp[random.randint(0, len(tmp)-1)] 
    
# def getNeighborRsuInfo(car):
#     neighborRsu = car.neighborRsu
#     if neighborRsu:
#         expectedTime = calculateTaskInQueue(neighborRsu) / Config.rsuProcessPerSecond
#         return (expectedTime, neighborRsu.meanDelay, neighborRsu)
#     else:
#         print("Don't has neighbor rsu")
#         input()
#         return (0.0, 0.0, None)

def getState(car, message, network):
    # print("car_{} get state for message id {}".format(car.id, message.stt))
    # print("len waitList of this car {}".format(len(car.waitList)))
    # Info of this message
    # res = [message.size, message.cpuCycle]
    # Info of this car
    # res.append(calculateTaskInQueue(car))
    res = []
    # res.append(car.meanDelayProcess)
    # res.append(car.meanDelaySendToCar)
    # res.append(car.meanDelaySendToRsu)
    # res.append(car.meanDelaySendToGnb)
    # Info of it's neighbor car
    # neighborCarInfo = getNeighborCarInfo(car)
    # res.append(neighborCarInfo[0])
    # res.append(neighborCarInfo[1])
    # Info of it's neighbor rsu
    # neighborRsuInfo = getNeighborRsuInfo(car)
    # res.append(neighborRsuInfo[0])
    # res.append(neighborRsuInfo[1])
    # Info of gnb
    res.append(car.meanDelaySendToRsu)
    res.append(car.meanDelaySendToGnb)
    res.append(car.neighborRsu.numTask)
    res.append(network.gnb.numTask)
    res = np.reshape(res, (1, len(res)))
    return res

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
    # 0: gnb, # 1: rsu
    logger.info("Car {} get action with message stt {}".format(car.id, message.stt))
    if car.optimizer is not None:
        currentState = getState(car, message, network)
        car.optimizer.updateState(message, currentState)
        # get values of all actions
        allActionValues = car.optimizer.getAllActionValues(currentState)
        logger.info("All action values {}".format(allActionValues))
        # get action by policy
        actionByPolicy = car.optimizer.policy(allActionValues)
        logger.info("Choose action {}".format(actionByPolicy))
        # Update memory
        car.optimizer.addToMemoryTmp(message, currentState, actionByPolicy)
    else:
        rand = random.random()
        if rand < Config.default_pl:
            actionByPolicy = 0
        else:
            actionByPolicy = 1
    # return tuple of action and object the message will be in
    if actionByPolicy == 0:
        res = (2, network.gnb)
    else:
        res = (1, car.neighborRsu)
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

