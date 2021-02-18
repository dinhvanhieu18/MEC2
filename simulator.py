# from carSimulator import *
# from rsuSimulator import *
# from gnbSimulator import *
from utils import *

#-----------------------------------Class Message------------------------------------------#

class Message:
    def __init__(self):
        self.stt = -1
        self.indexCar = []
        self.indexRsu = []
        self.sendTime = []
        self.receiveTime = []
        self.location = []
        self.currentTime = 0.0
        # self.currentLocation = 0
        self.isDone = False
        self.type = ""
        self.isDropt = False
        # location:
        # 0: car, 1:rsu, 2:gnb

#-------------------------------------------------------------------------------------------#



#------------------------------------Class Car----------------------------------------------#
class CarSimulator:
    def __init__(
        self,
        id,
        startTime,
    ):
        self.id = id
        self.startTime = startTime
        self.numMessage = 0
        self.preReceiveFromGnb = 0.0
        self.preReceiveFromRsu = 0.0
        self.preReceiveFromCar = 0.0
        self.waitList = []
        self.preProcess = 0.0

    def collectMessages(self, currentTime):
        if self.getPosition(currentTime) > Simulator.roadLength:
            return []
        if self.numMessage >= len(Simulator.listTimeMessages):
            return self.waitList
        tmp = self.waitList
        self.waitList = []
        res = []
        for mes in tmp:
            if mes.currentTime > currentTime + Simulator.cycleTime:
                self.waitList.append(mes)
            else:
                res.append(mes)
        curTime = Simulator.listTimeMessages[self.numMessage]
        while True:
            sendTime = self.startTime + curTime
            if sendTime > currentTime + Simulator.cycleTime:
                return res
            mes = Message()
            Simulator.setStt(mes)
            mes.indexCar.append(self.id)
            mes.sendTime.append(sendTime)
            mes.currentTime = sendTime
            mes.location.append(0)
            # mes.currentLocation = 0
            # mes.currentObject = self
            res.append(mes)
            self.numMessage += 1
            if (self.numMessage >= len(Simulator.listTimeMessages)):
                return res
            curTime = Simulator.listTimeMessages[self.numMessage]
    
    def working(self, message, currentTime):
        if message.isDone:
            startCar = Simulator.carList[message.indexCar[0]]
            self.sendToCar(startCar, message, currentTime)
            return

        rand = random.random()
        if rand < Simulator.pCarToCar:
            nearCar = self.getNearCar(currentTime)
            if nearCar:
                # print(f"Send from car {self.id} to car {nearCar.id}")
                self.sendToCar(nearCar, message, currentTime)
            else:
                # print(f"Not found car near with car {self.id}, car process")
                self.process(message, currentTime)

        elif rand < Simulator.pCarToCar + Simulator.pCarToRsu:
            nearRsu = self.getNearRsu(currentTime)
            if nearRsu:
                # print(f"Send from car {self.id} to rsu {nearRsu.id}")
                self.sendToRsu(nearRsu, message, currentTime)
            else:
                # print(f"Not found rsu near with car {car.id}, send to gnb")
                self.sendToGnb(message, currentTime)

        elif rand < Simulator.pCarToCar + Simulator.pCarToRsu + Simulator.pCarToGnb:
            # print(f"Send from car {self.id } to gnb")
            self.sendToGnb(message, currentTime)

        else:
            # print(f"Car {self.id} process")
            self.process(message, currentTime)

    def getPosition(self, currentTime):
        return Simulator.carSpeed * (currentTime - self.startTime)

    def sendToCar(self, car, message, currentTime):
        message.indexCar.append(car.id)
        tranferTime = getNext(1.0/Simulator.carCarMeanTranfer)
        selectedTime = max(car.preReceiveFromCar, message.currentTime)
        receiveTime = tranferTime + selectedTime
        message.receiveTime.append(receiveTime)
        car.preReceiveFromCar = receiveTime
        message.currentTime = receiveTime
        message.location.append(0)
        # message.currentLocation = 0
        if message.isDone:
            Simulator.output.append(message)
        elif message.currentTime > currentTime + Simulator.cycleTime:
            car.waitList.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

    def getNearCar(self, currentTime):
        minDis = Simulator.roadLength
        listRes = []
        for car in Simulator.carList:
            if car.id == self.id:
                continue
            if car.startTime > currentTime:
                continue
            distance = self.distanceToCar(car, currentTime)
            if distance > Simulator.carCoverRadius:
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

    def sendToRsu(self, rsu, message, currentTime):
        message.indexRsu.append(rsu.id)
        tranferTime = getNext(1.0/Simulator.carRsuMeanTranfer)
        selectedTime = max(rsu.preReceiveFromCar, message.currentTime)
        receiveTime = tranferTime + selectedTime
        message.receiveTime.append(receiveTime)
        rsu.preReceiveFromCar = receiveTime
        message.currentTime = receiveTime
        message.location.append(1)
        # message.currentLocation = 1
        if message.currentTime > currentTime + Simulator.cycleTime:
            rsu.waitList.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

    def getNearRsu(self, currentTime):
        minDis = 100000000
        listRes = []
        for rsu in Simulator.rsuList:
            distance = self.distanceToRsu(rsu, currentTime)
            if distance > Simulator.rsuCoverRadius:
                continue
            if distance < minDis:
                minDis = distance
                listRes = [rsu]
            elif distance == minDis:
                listRes.append(rsu)
        if listRes:
           return listRes[random.randint(0, len(listRes)-1)]
        else:
            return None 

    def sendToGnb(self, message, currentTime):
        tranferTime = getNext(1.0/Simulator.carGnbMeanTranfer)
        selectedTime = max(Simulator.gnb.preReceiveFromCar, message.currentTime)
        receiveTime = tranferTime + selectedTime
        message.receiveTime.append(receiveTime)
        Simulator.gnb.preReceiveFromCar = receiveTime
        message.currentTime = receiveTime
        message.location.append(2)
        # message.currentObject = Simulator.gnb
        if message.currentTime > currentTime + Simulator.cycleTime:
            Simulator.gnb.waitList.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

    def distanceToCar(self, car, currentTime):
        return abs(self.getPosition(currentTime) - car.getPosition(currentTime))

    def distanceToRsu(self, rsu, currentTime):
        position = self.getPosition(currentTime)
        return math.sqrt(
            pow(position - rsu.xcord, 2) + pow(rsu.ycord, 2) + pow(rsu.zcord, 2)
        )   

    def process(self, message, currentTime):
        input()
        selectedTime = max(message.currentTime, self.preProcess)
        processTime = getNext(Simulator.carProcessPerSecond)
        processedTime = selectedTime + processTime
        message.currentTime = processedTime
        message.isDone = True
        self.preProcess = processedTime
        startCar = Simulator.carList[message.indexCar[0]]
        if startCar.id == self.id:
            Simulator.output.append(message)
        elif startCar.getPosition(currentTime) > Simulator.roadLength \
           or self.distanceToCar(startCar, currentTime) > Simulator.carCoverRadius:
            message.isDropt = True
            Simulator.output.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

#-------------------------------------------------------------------------------------------#



#---------------------------------------Class Rsu-------------------------------------------#

class RsuSimulator:

    def __init__(
        self,
        id,
        xcord,
        ycord,
        zcord,
    ):
        self.id = id
        self.xcord = xcord
        self.ycord = ycord
        self.zcord = zcord
        self.nearRsuList = []
        self.waitList = []
        
        self.preReceiveFromCar = 0
        self.preReceiveFromRsu = 0
        self.preProcess = 0

    def findNearRsuList(self):
        minDis = 100000000
        listRes = []
        for rsu in Simulator.rsuList:
            if rsu.id == self.id:
                continue
            distance = self.distanceToRsu(rsu)
            if distance > Simulator.rsuCoverRadius:
                continue
            if distance < minDis:
                minDis = distance
                listRes = [rsu]
            elif distance == minDis:
                listRes.append(rsu)
        self.nearRsuList = listRes

    def collectMessages(self, currentTime):
        tmp = self.waitList
        self.waitList = []
        res = []
        for mes in tmp:
            if mes.currentTime > currentTime + Simulator.cycleTime:
                self.waitList.append(mes)
            else:
                res.append(mes)
        return res

    def working(self, message, currentTime):
        if message.isDone:
            startCar = Simulator.carList[message.indexCar[0]]
            self.sendToCar(startCar, message, currentTime)
            return

        rand = random.random()
        if rand < Simulator.pRsuToCar:
            nearCar = self.getNearCar(currentTime)
            if nearCar:
                # print(f"Send from rsu {self.id} to car {nearCar.id}")
                self.sendToCar(nearCar, message, currentTime)
            else:
                # print(f"Not found car near with rsu {self.id}, send to rsu")
                nearRsu = self.getNearRsu()
                if nearRsu:
                    # print(f"Send from rsu {self.id} to rsu {nearRsu.id}")
                    self.sendToRsu(nearRsu, message, currentTime)
                else:
                    # print(f"Not found rsu near with {self.id}, send to gnb")
                    self.sendToGnb(message, currentTime)

        elif rand < Simulator.pRsuToCar + Simulator.pRsuToRsu:
            nearRsu = self.getNearRsu()
            if nearRsu:
                # print(f"Send from rsu {self.id} to rsu {nearRsu.id}")
                self.sendToRsu(nearRsu, message, currentTime)
            else:
                # print(f"Not found rsu near with {self.id}, rsu process")
                self.process(message, currentTime)

        elif rand < Simulator.pRsuToCar + Simulator.pRsuToRsu + Simulator.pRsuToGnb:
            # print(f"Send from rsu {self.id} to gnb")
            self.sendToGnb(message, currentTime)

        else:
            # print(f"Rsu {self.id} process")
            self.process(message, currentTime)

    def sendToCar(self, car, message, currentTime):
        message.indexCar.append(car.id)
        tranferTime = getNext(1.0/Simulator.rsuCarMeanTranfer)
        selectedTime = max(car.preReceiveFromRsu, message.currentTime)
        receiveTime = tranferTime + selectedTime
        message.receiveTime.append(receiveTime)
        car.preReceiveFromRsu = receiveTime
        message.currentTime = receiveTime
        message.location.append(0)
        # message.currentLocation = 0
        if message.isDone:
            Simulator.output.append(message)
        elif message.currentTime > currentTime + Simulator.cycleTime:
            car.waitList.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

    def getNearCar(self, currentTime):
        minDis = 100000000
        listRes = []
        for car in Simulator.carList:
            if car.startTime > currentTime:
                continue
            distance = self.distanceToCar(car, currentTime)
            if distance > Simulator.rsuCoverRadius:
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

    def sendToRsu(self, rsu, message, currentTime):
        message.indexRsu.append(rsu.id)
        tranferTime = getNext(1.0/Simulator.rsuRsuMeanTranfer)
        selectedTime = max(rsu.preReceiveFromRsu, message.currentTime)
        receiveTime = tranferTime + selectedTime
        message.receiveTime.append(receiveTime)
        rsu.preReceiveFromRsu = receiveTime
        message.currentTime = receiveTime
        message.location.append(1)
        # message.currentLocation = 1
        if message.currentTime > currentTime + Simulator.cycleTime:
            rsu.waitList.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

    def getNearRsu(self):
        if self.nearRsuList:
           return self.nearRsuList[random.randint(0, len(self.nearRsuList)-1)]
        else:
            return None 

    def sendToGnb(self, message, currentTime):
        tranferTime = getNext(1.0/Simulator.rsuGnbMeanTranfer)
        selectedTime = max(Simulator.gnb.preReceiveFromRsu, message.currentTime)
        receiveTime = tranferTime + selectedTime
        message.receiveTime.append(receiveTime)
        Simulator.gnb.preReceiveFromRsu = receiveTime
        message.currentTime = receiveTime
        message.location.append(2)
        # message.currentObject = Simulator.gnb
        if message.currentTime > currentTime + Simulator.cycleTime:
            Simulator.gnb.waitList.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

    def distanceToCar(self, car, currentTime):
        positionCar = car.getPosition(currentTime)
        return math.sqrt(
            pow(positionCar - self.xcord, 2) + pow(self.ycord, 2) + pow(self.zcord, 2)
        ) 

    def distanceToRsu(self, rsu):
        return math.sqrt(
            pow(self.xcord - rsu.xcord, 2) + \
            pow(self.ycord - rsu.ycord, 2) + \
            pow(self.zcord - rsu.zcord, 2))   

    def process(self, message, currentTime):
        selectedTime = max(message.currentTime, self.preProcess)
        processTime = getNext(Simulator.rsuProcessPerSecond)
        processedTime = selectedTime + processTime
        message.currentTime = processedTime
        message.isDone = True
        self.preProcess = processedTime
        startCar = Simulator.carList[message.indexCar[0]]
        if startCar.getPosition(currentTime) > Simulator.roadLength \
           or self.distanceToCar(startCar, currentTime) > Simulator.rsuCoverRadius:
            message.isDropt = True
            Simulator.output.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))

#-------------------------------------------------------------------------------------------#



#---------------------------------------Class Gnb-------------------------------------------#

class GnbSimulator:
    def __init__(self):
        self.waitList = []
        
        self.preReceiveFromCar = 0
        self.preReceiveFromRsu = 0
        self.preProcess = 0

    def collectMessages(self, currentTime):
        tmp = self.waitList
        self.waitList = []
        res = []
        for mes in tmp:
            if mes.currentTime > currentTime + Simulator.cycleTime:
                self.waitList.append(mes)
            else:
                res.append(mes)
        return res

    def working(self, message, currentTime):
        if message.isDone:
            startCar = Simulator.carList[message.indexCar[0]]
            self.sendToCar(startCar, message, currentTime)
        else:
            self.process(message, currentTime)


    def sendToCar(self, car, message, currentTime):
        message.indexCar.append(car.id)
        tranferTime = getNext(1.0/Simulator.gnbCarMeanTranfer)
        selectedTime = max(car.preReceiveFromGnb, message.currentTime)
        receiveTime = tranferTime + selectedTime
        message.receiveTime.append(receiveTime)
        car.preReceiveFromGnb = receiveTime
        message.currentTime = receiveTime
        message.location.append(0)
        Simulator.output.append(message)

    def process(self, message, currentTime):
        selectedTime = max(message.currentTime, self.preProcess)
        processTime = getNext(Simulator.gnbProcessPerSecond)
        processedTime = selectedTime + processTime
        message.currentTime = processedTime
        message.isDone = True
        self.preProcess = processedTime
        startCar = Simulator.carList[message.indexCar[0]]
        if startCar.getPosition(currentTime) > Simulator.roadLength:
            message.isDropt = True
            Simulator.output.append(message)
        else:
            Simulator.q.put(PrioritizedItem((
                message.currentTime,
                message.stt,
                ),message))


#-------------------------------------------------------------------------------------------#



#---------------------------------------Class Simulator-------------------------------------#
class Simulator:
    gnb = GnbSimulator()
    rsuList = []
    carList = []
    output = []
    listTimeMessages = []
    stt = 0
    q = PriorityQueue()

    # gnb config
    gnbProcessPerSecond = 0
    gnbCarMeanTranfer = 0

    # rsu config
    rsuNumbers = 0
    xList = []
    yList = []
    zList = []
    rsuCoverRadius = 0
    rsuProcessPerSecond = 0
    rsuRsuMeanTranfer = 0
    rsuCarMeanTranfer = 0
    rsuGnbMeanTranfer = 0
    pRsuToCar = 0
    pRsuToRsu = 0
    pRsuToGnb = 0

    # car config
    carSpeed = 0
    carCoverRadius = 0
    carProcessPerSecond = 0
    carCarMeanTranfer = 0
    carRsuMeanTranfer = 0
    carGnbMeanTranfer = 0
    pCarToCar = 0
    pCarToRsu = 0
    pCarToGnb = 0

    # other
    carAppearStrategy = ""
    carPacketStrategy = ""
    simTime = 0
    cycleTime = 0
    roadLength = 0
    dumpDelayDetail = ""
    dumDelayGeneral = ""

    # result
    meanDelay = 0
    countDropt = 0
    totalOutsize = 0
    cumulativeDelay = 0
    maxDelay = 0

    # Test
    countType1 = 0
    countType2 = 0
    countType3 = 0
    
    @staticmethod
    def setStt(message):
        message.stt = Simulator.stt
        Simulator.stt += 1

    @staticmethod
    def main():
        for i in range(Simulator.rsuNumbers):
            rsu = RsuSimulator(
                id=i,
                xcord=Simulator.xList[i],
                ycord=Simulator.yList[i],
                zcord=Simulator.zList[i]
            )
            Simulator.rsuList.append(rsu)
        # print(len(Simulator.rsuList))
        for rsu in Simulator.rsuList:
            rsu.findNearRsuList()

        Simulator.prepareTimeMessages()
        print(len(Simulator.listTimeMessages))
        Simulator.carAppear()
        print(len(Simulator.carList))

        currentTime = 0
        while(currentTime < Simulator.simTime):
            Simulator.working(currentTime)
            Simulator.dumOutput(currentTime)
            currentTime += Simulator.cycleTime
        Simulator.finalDumpOutput()


    @staticmethod
    def prepareTimeMessages():
        try:
            f = open(Simulator.carPacketStrategy, "r")
            currentTime = 0
            for x in f:
                tmp = float(x)
                timeStartFromCar = currentTime + tmp
                currentTime = timeStartFromCar
                Simulator.listTimeMessages.append(timeStartFromCar)
        except:
            print("File packet not found !!!")
            exit()

    @staticmethod
    def carAppear():
        try:
            f = open(Simulator.carAppearStrategy, "r")
            currentTime = 0
            index = 0
            for x in f:
                tmp = float(x)
                timeStartCar = currentTime + tmp
                if timeStartCar > Simulator.simTime:
                    return
                car = CarSimulator(index, timeStartCar)
                Simulator.carList.append(car)
                index += 1
                currentTime = timeStartCar
        except:
            print("File car not found")
            exit()

    @staticmethod
    def collectMessages(currentTime):
        collectMessages = []
        for car in Simulator.carList:
            collectMessages.append(
                car.collectMessages(currentTime)
            )
        for rsu in Simulator.rsuList:
            collectMessages.append(
                rsu.collectMessages(currentTime)
            )
        collectMessages.append(
            Simulator.gnb.collectMessages(currentTime)
        )
        collectMessages = [
            i for sublist in collectMessages for i in sublist
        ]
        for mes in collectMessages:
            Simulator.q.put(PrioritizedItem((
                mes.currentTime,
                mes.stt,
                ),mes))
        # print(Simulator.q.qsize())

    @staticmethod
    def working(currentTime):
        # print("Working...")
        Simulator.collectMessages(currentTime)

        while not Simulator.q.empty():
            mes = Simulator.q.get().item
            # print(type(mes.currentObject))
            currentLocation = mes.location[-1]

            if currentLocation == 0:
                car = Simulator.carList[mes.indexCar[-1]]
                car.working(mes, currentTime)
                
            elif currentLocation == 1:
                rsu = Simulator.rsuList[mes.indexRsu[-1]]
                rsu.working(mes, currentTime)
            else:
                Simulator.gnb.working(mes, currentTime)


    @staticmethod
    def dumOutput(currentTime):
        if Simulator.output:
            Simulator.totalOutsize += len(Simulator.output)
            # f = open(Simulator.dumpDelayDetail, "a")
            for mes in Simulator.output:
                delay = mes.currentTime - mes.sendTime[0]
                Simulator.maxDelay = max(delay, Simulator.maxDelay)
                if mes.isDropt:
                    Simulator.countDropt += 1
                else:
                    Simulator.meanDelay += delay
                # if 1 in mes.location and 2 in mes.location:
                #     mes.type = 3
                #     Simulator.countType3 += 1
                # elif 1 in mes.location:
                #     mes.type = 1
                #     Simulator.countType1 += 1
                # else:
                #     mes.type = 2
                #     Simulator.countType2 += 1
                # f.write(f"{mes.sendTime[0]} \t {mes.currentTime} \t {delay} \t {mes.type} \t {Simulator.maxDelay} \n")
            Simulator.output = []

    @staticmethod
    def finalDumpOutput():
        Simulator.meanDelay = (Simulator.meanDelay + \
                Simulator.countDropt * Simulator.maxDelay) / Simulator.totalOutsize
        f = open(Simulator.dumDelayGeneral, "a")
        # f.write(f"{Simulator.carPacketStrategy} \t {Simulator.carAppearStrategy} \t \
        #     {Simulator.rsuNumbers} \t {Simulator.pRsuToCar} \t {Simulator.pRsuToRsu} \t \
        #     {Simulator.pRsuToGnb} \t {Simulator.pCarToCar} \t {Simulator.pCarToRsu}  \t \
        #     {Simulator.pCarToGnb} \t {Simulator.meanDelay} \t {Simulator.countDropt} \t \
        #     {Simulator.totalOutsize} \t {Simulator.countType1} \t {Simulator.countType2} \t \
        #     {Simulator.countType3} \n")
        f.write(f"{Simulator.carPacketStrategy} \t {Simulator.carAppearStrategy} \t \
            {Simulator.rsuNumbers} \t {Simulator.pRsuToCar} \t {Simulator.pRsuToRsu} \t \
            {Simulator.pRsuToGnb} \t {Simulator.pCarToCar} \t {Simulator.pCarToRsu}  \t \
            {Simulator.pCarToGnb} \t {Simulator.meanDelay} \t {Simulator.countDropt} \t \
            {Simulator.totalOutsize} \n")
        f.close()
        print("Done dumping final output!!!")

#-------------------------------------------------------------------------------------------#