from network import Network
from carSimulator import CarSimulator
from rsuSimulator import RsuSimulator
from gnbSimulator import GnbSimulator
from optimizers.carDQN import CarDQN
from optimizers.rsuDQN import RsuDQN
from config import Config

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
        )
        optimizer = RsuDQN(rsu=rsu)
        rsu.optimizer = optimizer
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
        car = CarSimulator(index, timeStartCar)
        optimizer = CarDQN(car=car)
        car.optimizer = optimizer
        res.append(car)
        index += 1
        currentTime = timeStartCar
    return res

if __name__=="__main__":
    main()
    # res = prepareTimeMessages()
    # print(len(res))
    # i = 1
    # j = 0
    # cnt = 0
    # while j < len(res):
    #     if res[j] < i:
    #         cnt +=1
    #     else:
    #         print(cnt)
    #         cnt = 0
    #         i += 1
    #     j += 1
