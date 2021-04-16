from config import Config
import os

def dumpOutputPerCycle(network, currentTime):
    if not network.output:
        return
    network.totalOutsize += len(network.output)
    fDelay = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.dumpDelayDetail}", "a")
    fMessage = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.messageDetail}", "a")
    #####################################################################################################
    # outputEachCar = [0] * len(network.carList)
    # for i in range(len(network.carList)):
    #     outputEachCar[i] = [0.0, 0.0, 0.0, 0, 0, 0]

    for mes in network.output:
        delay = mes.currentTime - mes.startTime
        network.maxDelay = max(delay, network.maxDelay)
        if mes.isDrop:
            network.countDrop += 1
        else:
            network.meanDelay += delay
        mes.setType()
    #     carID = mes.indexCar[0]
    #     if len(mes.indexRsu) > 0:
    #         if 2 in mes.locations:
    #             network.cntType3 += 1
    #             outputEachCar[carID][2] += delay
    #             outputEachCar[carID][5] += 1
    #         else:
    #             network.cntType2 += 1
    #             outputEachCar[carID][1] += delay
    #             outputEachCar[carID][4] += 1
    #     else:
    #         network.cntType1 += 1
    #         outputEachCar[carID][0] += delay
    #         outputEachCar[carID][3] += 1
    ##########################################################################################################
        fMessage.write(f"{mes.stt} {mes.indexCar[0]} {mes.startTime} {mes.currentTime} {delay} {mes.type} \n")
    meanDelay = (network.meanDelay + network.countDrop * network.maxDelay) / network.totalOutsize
    fDelay.write(f"{currentTime} \t {meanDelay} \t {network.maxDelay} \t {network.totalOutsize} \t {network.countDrop} \n")
    network.output = []
    # for i, v in enumerate(outputEachCar):
    #     car = network.carList[i]
    #     if car.getPosition(currentTime) > Config.roadLength \
    #         or car.startTime > currentTime:
    #             continue
    #     # print("Update car {}".format(car.id))
    #     # print("Before update")
    #     # print(car.optimizer.values)
    #     car.optimizer.update(values=[v[0], v[1]+v[2]], cnts=[v[3], v[4]+v[5]])
    #     # print("After update")
    #     # print(car.optimizer.values)
        
    #     rsu = car.neighborRsu
    #     # print("Update rsu {}".format(rsu.id))
    #     # print("Before update")
    #     # print(rsu.optimizer.values)
    #     rsu.optimizer.update(values=[v[2], v[1]], cnts=[v[5], v[4]])
    #     # print("After update")
    #     # print(rsu.optimizer.values)
          

def dumpOutputFinal(network):
    network.meanDelay = (network.meanDelay + \
            network.countDrop * network.maxDelay) / network.totalOutsize
    f = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.dumpDelayGeneral}", "a")
    f.write(f"{Config.packageStrategy} \t {Config.carAppearStrategy} \t {Config.rsuNumbers} \
              {Config.expName} \t {network.meanDelay} \t {network.countDrop} \t {network.totalOutsize} \
              {network.cntType1} \t {network.cntType2} \t {network.cntType3} {Config.default_pl} {Config.default_pr}\n")
    f.close()
    print("Done dumping final output!!!") 
