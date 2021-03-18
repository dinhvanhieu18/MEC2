from behaviorPolicy.epsilonGreedy import EpsilonGreedy
from optimizers.utils import calculateTaskInQueue
from config import Config
import random
import math
import numpy as np
from behaviorPolicy.epsilonGreedy import EpsilonGreedy
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import mean_squared_error

def getBehaviorPolicy(nActions, parameters):
    policy = EpsilonGreedy(
        nActions=nActions, 
        epsilon=parameters["epsilon"]
    )
    return policy

def buildModel(rsuDQN):
    model = Sequential()
    hidden_layers = Config.hiddenLayerConfigRsu
    model.add(Dense(hidden_layers[0], input_dim=rsuDQN.nStates, activation="relu"))
    for layer_size in hidden_layers[1:]:
        model.add(Dense(layer_size, activation="relu"))
    model.add(Dense(rsuDQN.nActions, activation="linear"))
    model.compile(loss=mean_squared_error, optimizer=Adam(lr=rsuDQN.alpha))
    return model

    
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
    

def getState(rsu, message):
    # Info of this message
    res = [message.size, message.cpuCycle]
    # Info of this rsu
    res.append(calculateTaskInQueue(rsu))
    res.append(rsu.meanDelayProcess)
    res.append(rsu.meanDelaySendToRsu)
    res.append(rsu.meanDelaySendToGnb)
    # Info of it's neighbor rsu
    neighborRsuInfo = getNeighborRsu(rsu)
    res.append(neighborRsuInfo[0])
    res.append(neighborRsuInfo[1])
    return (res, neighborRsuInfo[2])

def updateState(rsuDQN, message):
    print("Update State rsu {} with message id {}".format(rsuDQN.rsu.id, message.stt))
    print("Len memory Tmp:",len(rsuDQN.memory.memoryTmp))
    currentStateInfo = getState(rsuDQN.rsu, message)
    currentState = np.reshape(currentStateInfo[0], (1, len(currentStateInfo[0])))
    print("CurrentState:", currentState)
    if rsuDQN.memory.memoryTmp:
        preStateInfo = rsuDQN.memory.memoryTmp[-1]
        # Update nextState in experience
        preStateInfo[0][3] = currentState
        if preStateInfo[0][2] is not None: # Reward not None
            rsuDQN.memory.addToMemory(preStateInfo[0])
            # print("Update state")
            # print(preStateInfo)
            # print(len(rsuDQN.memory.memoryTmp))
            # rsuDQN.memory.memoryTmp.remove(preStateInfo)
            del rsuDQN.memory.memoryTmp[-1]
            print("delete state after update state")
            print("Len memory Tmp:", len(rsuDQN.memory.memoryTmp))
            # print(len(rsuDQN.memory.memoryTmp))
    print(rsuDQN.memory.memoryTmp)

def updateReward(rsuDQN, message):
    print("Update Reward rsu {} with message id {}".format(rsuDQN.rsu.id, message.stt))
    print("Len memory Tmp:",len(rsuDQN.memory.memoryTmp))
    rsuDQN.cnt += 1
    for i, stateInfo in enumerate(rsuDQN.memory.memoryTmp):
        if message.stt == stateInfo[1]:
            # Calculate reward
            if message.isDropt:
                reward = 0
            else:
                reward = 1.0 / (message.currentTime - stateInfo[2] + 0.01)
            # Update reward in experience
            print("Reward:", reward)
            stateInfo[0][2] = reward
            if stateInfo[0][3] is not None: # Next State not None
                rsuDQN.memory.addToMemory(stateInfo[0])
                # print("Update reward")
                # print(stateInfo)
                # print(len(rsuDQN.memory.memoryTmp))
                # rsuDQN.memory.memoryTmp.remove(stateInfo)
                rsuDQN.memory.memoryTmp[i] = None
                # print(len(rsuDQN.memory.memoryTmp))

    tmp = []
    for stateInfo in rsuDQN.memory.memoryTmp:
        if stateInfo is not None:
            tmp.append(stateInfo)
    rsuDQN.memory.memoryTmp = tmp
    print("Len memory Tmp:",len(rsuDQN.memory.memoryTmp))
    print(rsuDQN.memory.memoryTmp)

def addToMemoryTmp(rsuDQN, experience, message):
    rsuDQN.memory.addToMemoryTmp((experience, message.stt, message.currentTime))

    





            










