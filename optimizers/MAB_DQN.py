import random
from optimizers.optimizer import Optimizer
from optimizers.DQN import DQN
from optimizers.MAB import MAB
from config import Config
from optimizers.MAB_DQN_method import (
    getBehaviorPolicy,
    updateReward,
    addToMemoryTmp,
    chooseOptimizer,
)

class MAB_DQN(Optimizer):
    def __init__(self, agent_name, n_states, n_actions, policy_func=getBehaviorPolicy):
        self.agent_name = agent_name
        self.nStates = n_states
        self.nActions = n_actions
        self.probChooseF = 1
        self.policy = policy_func(parameters=Config.policyParamaters).getPolicy()
        self.MAB = MAB(agent_name, n_states, n_actions, getBehaviorPolicy)
        self.DQN = DQN(agent_name, n_states, n_actions, getBehaviorPolicy)
        self.stable = False

    def chooseOptimizer(self,func=chooseOptimizer):
        return func(self)

    def addToMemoryTmp(self, message, state, action, func=addToMemoryTmp):
        func(self, message, state, action)

    def updateReward(self, message, delay, func=updateReward):
        func(self, message, delay)
        

    def updateState(self, message, state):
        self.DQN.updateState(message, state)

    def getAllActionValues(self, state):
        optimizer = self.chooseOptimizer()
        return optimizer.getAllActionValues(state)