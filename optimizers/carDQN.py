import os
import numpy as np
from config import Config
from optimizers.optimizer import Optimizer
from optimizers.carDQN_method import (
    getBehaviorPolicy, getState,
    updateState, addToMemoryTmp, 
    updateReward, buildModel
    
)
from optimizers.utils import SequentialDequeMemory

class CarDQN(Optimizer):
    def __init__(self, car, policy_func=getBehaviorPolicy, policy_parameters=Config.policyParamatersCar):
        self.car = car
        self.nStates = Config.nStatesCar
        self.nActions = Config.nActionsCar
        self.alpha = Config.learningRateCar
        self.gamma = Config.disCountingFactorCar
        self.policy = policy_func(nActions=self.nActions, parameters=policy_parameters).getPolicy()
        self.onlineModel = buildModel(self)
        self.targetModel = buildModel(self)
        self.memory = SequentialDequeMemory(Config.queueCapacityCar)
        self.cnt = 0
        self.loadModelWeights()

    def updateOnlineModel(self, experience):
        currentState, action, instantaneousReward, nextState = experience
        actionTargetValues = self.onlineModel.predict(currentState)
        actionValuesForState = actionTargetValues[0]
        actionValuesForNextState = self.targetModel.predict(nextState)[0]
        maxNextStateValue = np.max(actionValuesForNextState)
        targetActionValue = instantaneousReward + self.gamma * maxNextStateValue
        actionValuesForState[action] = targetActionValue
        actionTargetValues[0] = actionValuesForState
        self.onlineModel.fit(currentState, actionTargetValues, epochs=1)

    def loadModelWeights(self):
        modelFile = os.path.join(os.path.join(Config.weightsDir, f"car_{self.car.id}.h5"))
        if os.path.exists(modelFile):
            self.onlineModel.load_weights(modelFile)
            self.targetModel.load_weights(modelFile)

    def saveModelWeights(self):
        # if os.path.exists(Config.weightsDir):
        #     os.mkdir(Config.weightsDir)
        # modelFile = f"{Config.weightsDir}/car_{self.car.id}.h5"
        # self.onlineModel.save_weights(modelFile, overwrite=True)
        pass

    def getState(self, message, func=getState):
        return func(self.car, message)

    def updateState(self, message, func=updateState):
        func(self, message)

    def updateReward(self, message, func=updateReward):
        func(self, message)

    def addToMemoryTmp(self, experience, message, func=addToMemoryTmp):
        func(self, experience, message)  

    def replayExperienceFromMemory(self):
        if self.memory.getMemorySize() < Config.batchSizeCar:
            return
        experienceBatch = self.memory.getRandomBatchForReplay(batchSize=Config.batchSizeCar)
        print("replay experience with {} experience".format(len(experienceBatch)))
        for experience in experienceBatch:
            self.updateOnlineModel(experience)

    def update(self):
        # self.replayExperienceFromMemory()
        if self.cnt % 10 == 0:
            self.replayExperienceFromMemory()
        if self.cnt % Config.timeToUpdateTargetModelCar == 0:
            self.saveModelWeights()
            self.targetModel.set_weights(self.onlineModel.get_weights())
        

    

      
    



        