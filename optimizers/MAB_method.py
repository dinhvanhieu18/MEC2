from config import Config
from behaviorPolicy.epsilonDecay import EpsilonDecay
from behaviorPolicy.sigmoidExplore import SigmoidExplore
from utils import logger

def getBehaviorPolicy(parameters):
    policy = SigmoidExplore( 
        epsilon=parameters["epsilon"],
        w=parameters["w"]
    )
    return policy

def addToMemoryTmp(MAB, message, state, action):
    MAB.memory[message.stt] = action

def updateReward(MAB, message, delay):
    logger.info("Update reward for {}".format(MAB.agent_name))
    # logger.info("Pre update reward")
    # logger.info("Memory {}".format(MAB.memory))
    # logger.info("Values {}".format(MAB.values))
    # logger.info("Cnt Take Actions {}".format(MAB.cntTakeAction))
    # action = MAB.memory[message.stt]
    # MAB.cntTakeAction[action] += 1
    # reward = - delay
    # # logger.info("Reward {}".format(reward))
    # learningRate = 1 / MAB.cntTakeAction[action]
    # MAB.values[action] = (1 - learningRate) * MAB.values[action] + learningRate * reward
    # # MAB.values[action] = (1 - Config.learningRateMAB) * MAB.values[action] + Config.learningRateMAB * reward

    # del MAB.memory[message.stt]
    # logger.info("After update reward")
    # logger.info("Memory {}".format(MAB.memory))
    # logger.info("Values {}".format(MAB.values))
    logger.info("Pre update reward: memory: {}, values: {}, cntTakeAction: {}".format(MAB.memory, MAB.values, MAB.cntTakeAction))
    action = MAB.memory[message.stt]
    MAB.cntTakeAction[action] += 1
    reward = -delay
    learningRate = 1 / MAB.cntTakeAction[action]
    MAB.values[action] = (1 - learningRate) * MAB.values[action] + learningRate * reward
    del MAB.memory[message.stt]
    logger.info("After update reward: memory: {}, values: {}, cntTakeAction: {}".format(MAB.memory, MAB.values, MAB.cntTakeAction))

    
