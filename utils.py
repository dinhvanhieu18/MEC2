import json
import argparse
import math
import random
import os
from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from config import Config
import logging
try:
    os.makedirs(f"{os.getcwd()}/{Config.weightsFolder}/{Config.expName}")
    os.makedirs(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}")
except:
    pass
try:
    os.remove(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.dumpDelayDetail}")
    os.remove(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.messageDetail}")
except:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.loggingFile}", 
            mode="w"
        )
    ]
)
logger = logging.getLogger()

def getNext(x):
    return -math.log(1.0 - random.random()) / x

@dataclass(order=True)
class PrioritizedItem:
    priority: (float, int)
    item: object = field()

def calculateTaskInQueue(obj):
    res = 0
    for mes in obj.waitList:
        if mes.isDone:
            continue
        res += mes.cpuCycle
    return res

def update(message, network):
    # index_list_car = -1
    # index_list_rsu = -1
    # index_list_receiveTime = -1
    # # print("Update message ", message.stt)
    # # for attr in dir(message):
    # #     print("obj.{} = {}".format(attr, getattr(message, attr)))
    # # input()
    # for i, location in enumerate(message.locations):
    #     # print("i=", i)
    #     # ignore the last index car (had been updated before)
    #     if len(message.indexCar) > 1:
    #         if not message.isDrop and i == len(message.locations) - 1: 
    #             # print("Break")
    #             break
    #     # ignor the last index rsu incase rsu1 ->rsu2 -> rsu1
    #     if len(message.indexRsu) == 3:
    #         if message.isDrop and i == len(message.locations) - 1:
    #             break
    #         if not message.isDrop and i == len(message.locations) - 2:
    #             break
    
    #     if location == 0:
    #         index_list_car += 1
    #         car_id = message.indexCar[index_list_car]
    #         obj = network.carList[car_id]
    #     elif location == 1:
    #         index_list_rsu += 1
    #         rsu_id = message.indexRsu[index_list_rsu]
    #         obj = network.rsuList[rsu_id]
    #     else:
    #         obj = network.gnb
    #     if i == 0:
    #         receiveTime = message.startTime
    #     else:
    #         index_list_receiveTime += 1
    #         receiveTime = message.receiveTime[index_list_receiveTime]
    #     # calculate delay for this object
    #     currentTime = message.currentTime
    #     delay = currentTime - receiveTime
    #     # print("delay=", delay)
    #     # for attr in dir(obj):
    #     #     print("obj.{} = {}".format(attr, getattr(obj, attr)))
    #     # input()
    #     # Check if message is drop, set delay to max delay in config
    #     obj.cnt += 1
    #     if message.isDrop:
    #         delay = Config.maxDelay
    #         obj.cntDrop += 1
    #     # obj.meanDelay += (delay - obj.meanDelay) / obj.cnt
    #     obj.meanDelay = a * obj.meanDelay + (1 - a) * delay
    #     obj.maxDelay = max(obj.maxDelay, delay)
    #     # Check if message is process by this object
    #     if (i == len(message.locations) - 2 and not message.isDrop) or \
    #        (i == len(message.locations) - 1):
    #         obj.cntProcess += 1
    #         # obj.meanDelayProcess += (delay - obj.meanDelayProcess) / obj.cntProcess
    #         obj.meanDelayProcess = a * obj.meanDelayProcess + (1 - a) * delay
    #     # else update with next location
    #     else:
    #         next_location = message.locations[i+1]
    #         if next_location == 0:
    #             obj.cntSendToCar += 1
    #             # obj.meanDelaySendToCar += (delay - obj.meanDelaySendToCar) / obj.cntSendToCar
    #             obj.meanDelaySendToCar = a * obj.meanDelaySendToCar + (1 - a) * delay
    #         elif next_location == 1:
    #             obj.cntSendToRsu += 1
    #             # obj.meanDelaySendToRsu += (delay - obj.meanDelaySendToRsu) / obj.cntSendToRsu
    #             obj.meanDelaySendToRsu = a * obj.meanDelaySendToRsu + (1 - a) * delay
    #         else:
    #             obj.cntSendToGnb += 1
    #             # obj.meanDelaySendToGnb += (delay - obj.meanDelaySendToGnb) / obj.cntSendToGnb
    #             obj.meanDelaySendToGnb = a * obj.meanDelaySendToGnb + (1 - a) * delay
    #     # for attr in dir(obj):
    #     #     print("obj.{} = {}".format(attr, getattr(obj, attr)))
    #     # input()
    #     # Update reward
    #     if location != 2:
    #         obj.optimizer.updateReward(message, delay)

    delay = delayForCar = delayForRsu = message.currentTime - message.startTime
    carID = message.indexCar[0]
    car = network.carList[carID]
    rsu = car.neighborRsu
    if message.isDrop:
        delayForCar = max(delay, car.maxDelay)
        delayForRsu = max(delay, rsu.maxDelay)
    car.maxDelay = max(car.maxDelay, delayForCar)
    car.optimizer.updateReward(message, delayForCar)
    if len(message.indexRsu) == 0:
        typeMessage = 1
    else:
        if 2 in message.locations:
            typeMessage = 3
        else:
            typeMessage = 2
        if message.indexRsu[0] == rsu.id:
            rsu.maxDelay = max (rsu.maxDelay, delayForRsu)
            rsu.optimizer.updateReward(message, delayForRsu)
    # Update meanDelay
    a = Config.decayRateMean
    if typeMessage == 1:
        car.meanDelay = a * car.meanDelay + (1 - a) * delayForCar if car.meanDelay > 0 else delayForCar
        car.meanDelaySendToGnb = a * car.meanDelaySendToGnb + (1 - a) * delayForCar if car.meanDelaySendToGnb > 0 else delayForCar
    else:
        car.meanDelaySendToRsu = a * car.meanDelaySendToRsu + (1 - a) * delayForCar if car.meanDelaySendToRsu > 0 else delayForCar
        if message.indexRsu[0] != rsu.id:
            return
        rsu.meanDelay = a * rsu.meanDelay + (1 - a) * delayForRsu if rsu.meanDelay > 0 else delayForRsu
        if typeMessage == 2:
            rsu.meanDelayProcess = a * rsu.meanDelayProcess + (1 - a) * delayForRsu if rsu.meanDelayProcess > 0 else delayForRsu
        else:
            rsu.meanDelaySendToGnb = a * rsu.meanDelaySendToGnb + (1 - a) * delayForRsu if rsu.meanDelaySendToGnb > 0 else delayForRsu


        
        
        



    

