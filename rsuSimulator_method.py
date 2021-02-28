import random
from config import Config
# from optimizer import optimizer

def getNearCar(rsu, currentTime, network):
    minDis = 10000000
    listRes = []
    for car in network.carList:
        if car.startTime > currentTime:
            continue
        distance = rsu.distanceToCar(car, currentTime)
        if distance > Config.rsuCoverRadius:
            continue
        if distance < minDis:
            minDis = distance
            listRes = [car]
        elif distance == minDis:
            listRes.append(car)
    if listRes:
        return listRes[random.randint(0, len(listRes)-1)]
    else:
        return None 

def getNearRsu(rsu):
    if rsu.nearRsuList:
        return rsu.nearRsuList[random.randint(0, len(rsu.nearRsuList)-1)]
    else:
        return None

def getAction(rsu, message, currentTime, network, optimizer=None):
    pRsuToCar = 0.0
    pRsuToRsu = 0.0
    pRsuToGnb = 0.5
    rand = random.random()
    if rand < pRsuToCar:
        nearCar = rsu.getNearCar(currentTime, network)
        if nearCar:
            return (0, nearCar)
        else:
            return (2, network.gnb)
    elif rand < pRsuToCar + pRsuToRsu:
        nearRsu = rsu.getNearRsu()
        if nearRsu:
            return (1, nearRsu)
        else:
            return (2, network.gnb)
    elif rand < pRsuToCar + pRsuToRsu + pRsuToGnb:
        return (2, network.gnb)
    else:
        return (3, None)

