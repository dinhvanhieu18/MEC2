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

if not os.path.exists(f"{os.getcwd()}/{Config.weightsFolder}"):
    os.mkdir(f"{os.getcwd()}/{Config.weightsFolder}")
if not os.path.exists(f"{os.getcwd()}/{Config.weightsFolder}/{Config.expName}"):
    os.mkdir(f"{os.getcwd()}/{Config.weightsFolder}/{Config.expName}")

if not os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}"):
    os.mkdir(f"{os.getcwd()}/{Config.resultsFolder}")

if not os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}"):
    os.mkdir(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}")
else:
    if os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.messageDetail}"):
        os.remove(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.messageDetail}")
    if os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.loggingFile}"):
        os.remove(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.loggingFile}")

logging.basicConfig(filename=f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.loggingFile}", 
                    format='%(levelname)s:%(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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
    # print("Update message ", message.stt)
    # for attr in dir(message):
    #     print("obj.{} = {}".format(attr, getattr(message, attr)))
    # input()
    for i, location in enumerate(message.locations):
        # print("i=", i)
        # ignore the last index car (had been updated before)
        if len(message.indexCar) > 1:
            if not message.isDrop and i == len(message.locations) - 1: 
                # print("Break")
                break
        # ignor the last index rsu incase rsu1 ->rsu2 -> rsu1
        if len(message.indexRsu) == 3:
            if message.isDrop and i == len(message.locations) - 1:
                break
            if not message.isDrop and i == len(message.locations) - 2:
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
        # print("delay=", delay)
        # for attr in dir(obj):
        #     print("obj.{} = {}".format(attr, getattr(obj, attr)))
        # input()
        # Check if message is drop, set delay to max delay in config
        obj.cnt += 1
        if message.isDrop:
            delay = Config.maxDelay
            obj.cntDrop += 1
        # obj.meanDelay += (delay - obj.meanDelay) / obj.cnt
        obj.meanDelay = Config.decayRateMean * obj.meanDelay + (1 - Config.decayRateMean) * delay
        obj.maxDelay = max(obj.maxDelay, delay)
        # Check if message is process by this object
        if (i == len(message.locations) - 2 and not message.isDrop) or \
           (i == len(message.locations) - 1):
            obj.cntProcess += 1
            # obj.meanDelayProcess += (delay - obj.meanDelayProcess) / obj.cntProcess
            obj.meanDelayProcess = Config.decayRateMean * obj.meanDelayProcess + (1 - Config.decayRateMean) * delay
        # else update with next location
        else:
            next_location = message.locations[i+1]
            if next_location == 0:
                obj.cntSendToCar += 1
                # obj.meanDelaySendToCar += (delay - obj.meanDelaySendToCar) / obj.cntSendToCar
                obj.meanDelaySendToCar = Config.decayRateMean * obj.meanDelaySendToCar + (1 - Config.decayRateMean) * delay
            elif next_location == 1:
                obj.cntSendToRsu += 1
                # obj.meanDelaySendToRsu += (delay - obj.meanDelaySendToRsu) / obj.cntSendToRsu
                obj.meanDelaySendToRsu = Config.decayRateMean * obj.meanDelaySendToRsu + (1 - Config.decayRateMean) * delay
            else:
                obj.cntSendToGnb += 1
                # obj.meanDelaySendToGnb += (delay - obj.meanDelaySendToGnb) / obj.cntSendToGnb
                obj.meanDelaySendToGnb = Config.decayRateMean * obj.meanDelaySendToGnb + (1 - Config.decayRateMean) * delay
        # for attr in dir(obj):
        #     print("obj.{} = {}".format(attr, getattr(obj, attr)))
        # input()
        # Update reward
        if location != 2:
            obj.optimizer.updateReward(message, delay)

        
        
        



    

