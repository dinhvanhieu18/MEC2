import os
import numpy as np
from config import Config
from optimizers.optimizer import Optimizer
from optimizers.MAB_method import (
    getBehaviorPolicy,
    addToMemoryTmp, 
    updateReward,
)

class MAB(Optimizer):
    def __init__(self, agent_name, n_states, n_actions, policy_func=getBehaviorPolicy):
        self.agent_name = agent_name
        self.nActions = n_actions
        self.policy = policy_func(parameters=Config.policyParamaters).getPolicy()
        self.values = [0] * self.nActions
        self.cntTakeAction = [0] * self.nActions
        self.memory = {}

    def addToMemoryTmp(self, message, state, action, func=addToMemoryTmp):
        func(self, message, state, action)

    def updateReward(self, message, delay, func=updateReward):
        func(self, message, delay)

    def getAllActionValues(self, state=None):
        return list(self.values)

    # def update(self, values, cnts):
    #     for i in range(len(values)):
    #         if cnts[i] == 0:
    #             continue
    #         self.cntTakeAction[i] += cnts[i]
    #         reward = - values[i] / cnts[i]
    #         learningRate = 1 / self.cntTakeAction[i]
    #         self.values[i] = (1 - learningRate) * self.values[i] + learningRate * reward
        
        

    

      
    



        
