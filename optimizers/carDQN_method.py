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

def buildModel(carDQN):
    model = Sequential()
    hidden_layers = Config.hiddenLayerConfigCar
    model.add(Dense(hidden_layers[0], input_dim=carDQN.nStates, activation="relu"))
    for layer_size in hidden_layers[1:]:
        model.add(Dense(layer_size, activation="relu"))
    model.add(Dense(carDQN.nActions, activation="linear"))
    model.compile(loss=mean_squared_error, optimizer=Adam(lr=carDQN.alpha))
    return model

def getNeighborCar(car):
    def sortFunc(e):
        return e[0] * e[1]
    tmp = []
    for car_ in car.neighborCars:
        expectedTime = calculateTaskInQueue(car_) / Config.carProcessPerSecond
        tmp.append((expectedTime, car_.meanDelay, car_))
    tmp.sort(key=sortFunc)
    if not tmp:
        return (0.0, 0.0, None)
    rand = random.random()
    if rand < 0.5:
        return tmp[0]
    else:
        return tmp[random.randint(0, len(tmp)-1)] 
    
def getNeighborRsu(car):
    neighborRsu = car.neighborRsu
    if neighborRsu:
        expectedTime = calculateTaskInQueue(neighborRsu) / Config.rsuProcessPerSecond
        return (expectedTime, neighborRsu.meanDelay, neighborRsu)
    else:
        return (0.0, 0.0, None)

def getState(car, message):
    # Info of this message
    res = [message.size, message.cpuCycle]
    # Info of this car
    res.append(calculateTaskInQueue(car))
    res.append(car.meanDelayProcess)
    res.append(car.meanDelaySendToCar)
    res.append(car.meanDelaySendToRsu)
    res.append(car.meanDelaySendToGnb)
    # Info of it's neighbor car
    neighborCarInfo = getNeighborCar(car)
    res.append(neighborCarInfo[0])
    res.append(neighborCarInfo[1])
    # Info of it's neighbor rsu
    neighborRsuInfo = getNeighborRsu(car)
    res.append(neighborRsuInfo[0])
    res.append(neighborRsuInfo[1])
    return (res, neighborCarInfo[2], neighborRsuInfo[2])

def updateState(carDQN, message):
    print("Update State car {} with message id {}".format(carDQN.car.id, message.stt))
    print("Len memory Tmp:",len(carDQN.memory.memoryTmp))
    currentStateInfo = getState(carDQN.car, message)
    currentState = np.reshape(currentStateInfo[0], (1, len(currentStateInfo[0])))
    print("CurrentState:", currentState)
    if carDQN.memory.memoryTmp:
        preStateInfo = carDQN.memory.memoryTmp[-1]
        # Update nextState in experience
        preStateInfo[0][3] = currentState
        if preStateInfo[0][2] is not None: # Reward not None
            carDQN.memory.addToMemory(preStateInfo[0])
            # print("Update state")
            # print(preStateInfo)
            # print(len(carDQN.memory.memoryTmp))
            # carDQN.memory.memoryTmp.remove(preStateInfo)
            del carDQN.memory.memoryTmp[-1]
            print("delete state after update state")
            print("Len memory Tmp:", len(carDQN.memory.memoryTmp))
            # print(len(carDQN.memory.memoryTmp))
    print(carDQN.memory.memoryTmp)

def updateReward(carDQN, message):
    print("Update Reward car {} with message id {}".format(carDQN.car.id, message.stt))
    print("Len memory Tmp:",len(carDQN.memory.memoryTmp))
    carDQN.cnt += 1
    for i, stateInfo in enumerate(carDQN.memory.memoryTmp):
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
                carDQN.memory.addToMemory(stateInfo[0])
                # print("Update reward")
                # print(stateInfo)
                # print(len(carDQN.memory.memoryTmp))
                # carDQN.memory.memoryTmp.remove(stateInfo)
                del carDQN.memory.memoryTmp[i]
                print("Delete state after update reward")
                print("Len memory Tmp:",len(carDQN.memory.memoryTmp))
                # print(len(carDQN.memory.memoryTmp))
    print(carDQN.memory.memoryTmp)

def addToMemoryTmp(carDQN, experience, message):
    carDQN.memory.addToMemoryTmp((experience, message.stt, message.currentTime))

    





            










