from behaviorPolicy.epsilonDecay import EpsilonDecay
from behaviorPolicy.sigmoidExplore import SigmoidExplore
from config import Config
import numpy as np

def getBehaviorPolicy(parameters):
    policy = SigmoidExplore( 
        epsilon=parameters["epsilon"],
        w=parameters["w"]
    )
    return policy

def chooseOptimizer(MAB_DQN):
    if MAB_DQN.stable:
        return MAB_DQN.DQN
    else:
        return MAB_DQN.MAB

def addToMemoryTmp(MAB_DQN, message, state, action):
    MAB_DQN.DQN.addToMemoryTmp(message, state, action)
    if not MAB_DQN.stable:
        MAB_DQN.MAB.addToMemoryTmp(message, state, action)
    

def updateReward(MAB_DQN, message, delay):
    state = MAB_DQN.DQN.updateReward(message, delay)
    if not MAB_DQN.stable:
        MAB_DQN.MAB.updateReward(message, delay)
        if state is None:
            return
        # Update probChooseF
        if MAB_DQN.probChooseF > Config.minprobChooseF:
            MAB_DQN.probChooseF *= Config.decayRateProbChooseF
        # Update online model with ground truth is values of MAB
        values = MAB_DQN.MAB.getAllActionValues()
        ytrain = np.array([values])
        MAB_DQN.DQN.onlineModel.fit(state, ytrain, epochs=1)
        output = MAB_DQN.DQN.onlineModel.predict(state)[0]
        # Check status stable
        v = 0
        for i in range(len(values)):
            v1 = values[i]
            v2 = output[i]
            diff = abs(v1 - v2)
            rate = 1 - diff / (abs(v1) + abs(v2) + 0.00000001)
            v += rate
        v /= len(values)
        if v > Config.threadHoldStable and MAB_DQN.probChooseF <= Config.minprobChooseF:
            MAB_DQN.stable = True
            MAB_DQN.DQN.stable = True
            MAB_DQN.DQN.targetModel.set_weights(MAB_DQN.DQN.onlineModel.get_weights())



        

    
    
    


