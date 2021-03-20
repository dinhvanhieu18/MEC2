from network import Network
from carSimulator import CarSimulator
from rsuSimulator import RsuSimulator
from gnbSimulator import GnbSimulator
from optimizers.DQN import DQN
from config import Config
import os

def main():
    gnb = GnbSimulator()
    rsuList= getRsuList()
    print(len(rsuList))
    carList = carAppear()
    print(len(carList))
    listTimeMessages = prepareTimeMessages()
    print(len(listTimeMessages))
    network = Network(
        gnb=gnb,
        rsuList=rsuList,
        carList=carList,
        listTimeMessages=listTimeMessages,
    )
    network.run()

def getRsuList():
    res = []
    for i in range(Config.rsuNumbers):
        rsu = RsuSimulator(
            id=i,
            xcord=Config.xList[i],
            ycord=Config.yList[i],
            zcord=Config.zList[i],
            optimizer=DQN(
                agent_name=f"rsu_{i}", 
                n_states=Config.nStatesRsu, 
                n_actions=Config.nActionsRsu,
            )
        )
        res.append(rsu)
    return res

def prepareTimeMessages():
    try:
        f = open(Config.carPacketStrategy, "r")
    except:
        print("File packet not found !!!")
        exit()
    currentTime = 0
    res = []
    for x in f:
        tmp = float(x)
        timeStartFromCar = currentTime + tmp
        currentTime = timeStartFromCar
        res.append(timeStartFromCar)
    return res

def carAppear():
    try:
        f = open(Config.carAppearStrategy, "r")
    except:
        print("File car not found")
        exit()
    res = []
    currentTime = 0
    index = 0
    for x in f:
        tmp = float(x)
        timeStartCar = currentTime + tmp
        if timeStartCar > Config.simTime:
            return res
        car = CarSimulator(
            id=index, 
            startTime=timeStartCar,
            optimizer=DQN(
                agent_name=f"car_{index}",
                n_states=Config.nStatesCar,
                n_actions=Config.nActionsCar,
            )
        )
        res.append(car)
        index += 1
        currentTime = timeStartCar
    return res


if __name__=="__main__":
    if not os.path.exists(f"{os.getcwd()}/{Config.weightsFolder}"):
        os.mkdir(f"{os.getcwd()}/{Config.weightsFolder}")
    if not os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}"):
        os.mkdir(f"{os.getcwd()}/{Config.resultsFolder}")
    main()
