from config import Config
from behaviorPolicy.epsilonDecay import EpsilonDecay
from utils import getLogger
logger = getLogger

def getBehaviorPolicy(parameters):
    policy = EpsilonDecay( 
        epsilon=parameters["epsilon"],
        min_epsilon=parameters["min_epsilon"],
        epsilon_decay_rate=parameters["epsilon_decay_rate"],
    )
    return policy

def addToMemoryTmp(MAB, message, state, action):
    MAB.memory[message.stt] = action

def updateReward(MAB, message, delay):
    logger.info("Update reward for {}".format(MAB.agent_name))
    logger.info("Pre update reward")
    logger.info("Memory {}".format(MAB.memory))
    logger.info("Values {}".format(MAB.values))
    action = MAB.memory[message.stt]
    reward = 1 / (delay + 0.01)
    logger.info("Reward {}".format(reward))
    MAB.values[action] = (1 - Config.learningRateMAB) * MAB.values[action] + Config.learningRateMAB * reward
    del MAB.memory[message.stt]
    logger.info("After update reward")
    logger.info("Memory {}".format(MAB.memory))
    logger.info("Values {}".format(MAB.values))
