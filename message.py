from config import Config
class Message:
    cnt = 0
    def __init__(self, indexCar, time, size=1, cpuCycle=1, ttl=Config.ttl):
        self.size = size
        self.cpuCycle = cpuCycle
        self.ttl = ttl
        self.stt = Message.cnt 
        Message.cnt += 1
        self.indexCar = [indexCar] 
        self.indexRsu = []
        self.sendTime = [time]
        self.receiveTime = []
        self.locations = [0] # locations 0: car, 1:rsu, 2:gnb
        self.currentTime = time
        self.isDone = False
        self.isDrop = False
        self.type = ""

    def setType(self):
        for location in self.locations:
            if location == 0:
                self.type += "car_"
            elif location == 1:
                self.type += "rsu_"
            else:
                self.type += "gnb_"
        self.type = self.type[:-1]

# a = Message(indexCar=1, time = 2)
# a.locations.append(1)
# a.locations.append(2)
# a.locations.append(0)
# print(a.stt)
# a.setType()
# print(a.type)
