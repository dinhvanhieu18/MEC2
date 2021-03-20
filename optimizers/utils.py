from collections import deque
import random

class SequentialDequeMemory:
    def __init__(self, queueCapacity=2000):
        self.queueCapacity = 2000
        self.memory = deque(maxlen=self.queueCapacity)
        self.memoryTmp = []

    def addToMemory(self, experienceTuple):
        self.memory.append(experienceTuple)

    def getRandomBatchForReplay(self, batchSize=32):
        return random.sample(self.memory, batchSize)

    def getMemorySize(self):
        return len(self.memory)

    def addToMemoryTmp(self, tmpTuple):
        self.memoryTmp.append(tmpTuple)