import json
import argparse
import math
import random
from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from config import Config


def getConfig():
    """
    Get config

    """
    # Get config path from user
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", help="Path to config.json")
    args = parser.parse_args()

    # Load config
    with open(args.config_path, "r") as f:
        config = json.load(f)

    return config

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
    index_list_car = -1
    index_list_rsu = -1
    index_list_receiveTime = -1
    print("Update message ", message.stt)
    for attr in dir(message):
        print("obj.{} = {}".format(attr, getattr(message, attr)))
    input()
    for i, location in enumerate(message.locations):
        print("i=", i)
        if i == len(message.locations) - 1 and not message.isDrop:
            if len(message.locations) > 1:
                print("Break")
                break
        if location == 0:
            index_list_car += 1
            car_id = message.indexCar[index_list_car]
            obj = network.carList[car_id]
        elif location == 1:
            index_list_rsu += 1
            rsu_id = message.indexRsu[index_list_rsu]
            obj = network.rsuList[rsu_id]
        else:
            obj = network.gnb
        if i == 0:
            receiveTime = message.startTime
        else:
            index_list_receiveTime += 1
            receiveTime = message.receiveTime[index_list_receiveTime]
        # calculate delay for this object
        currentTime = message.currentTime
        delay = currentTime - receiveTime
        print("delay=", delay)
        for attr in dir(obj):
            print("obj.{} = {}".format(attr, getattr(obj, attr)))
        input()
        # Check if message is drop, set delay to max delay in config
        obj.cnt += 1
        if message.isDrop:
            delay = Config.maxDelay
            obj.cntDrop += 1
        obj.meanDelay += (delay - obj.meanDelay) / obj.cnt
        obj.maxDelay = max(obj.maxDelay, delay)
        # Check if message is process by this object
        if (i == len(message.locations) - 2 and not message.isDrop) or \
           (i == len(message.locations) - 1):
            obj.cntProcess += 1
            obj.meanDelayProcess += (delay - obj.meanDelayProcess) / obj.cntProcess
        # else update with next location
        else:
            next_location = message.locations[i+1]
            if next_location == 0:
                obj.cntSendToCar += 1
                obj.meanDelaySendToCar += (delay - obj.meanDelaySendToCar) / obj.cntSendToCar
            elif next_location == 1:
                obj.cntSendToRsu += 1
                obj.meanDelaySendToRsu += (delay - obj.meanDelaySendToRsu) / obj.cntSendToRsu
            else:
                obj.cntSendToGnb += 1
                obj.meanDelaySendToGnb += (delay - obj.meanDelaySendToGnb) / obj.cntSendToGnb
        for attr in dir(obj):
            print("obj.{} = {}".format(attr, getattr(obj, attr)))
        input()
        # Update reward
        if location != 2:
            print("Update reward")
            print("Pre update")
            for attr in dir(obj.optimizer):
                print("obj.{} = {}".format(attr, getattr(obj.optimizer, attr)))
            input()
            obj.optimizer.updateReward(message, delay)
            print("After update")
            for attr in dir(obj.optimizer):
                print("obj.{} = {}".format(attr, getattr(obj.optimizer, attr)))
            input()

        
        
        



    

