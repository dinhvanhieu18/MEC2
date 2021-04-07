from config import Config
import os

def dumpOutputPerCycle(network, currentTime):
    if not network.output:
        return
    network.totalOutsize += len(network.output)
    fDelay = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.dumpDelayDetail}", "a")
    fMessage = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.messageDetail}", "a")
    for mes in network.output:
        delay = mes.currentTime - mes.startTime
        network.maxDelay = max(delay, network.maxDelay)
        if mes.isDrop:
            network.countDrop += 1
        else:
            network.meanDelay += delay
        mes.setType()
        if mes.type == "car_gnb_car":
            network.cntType1 += 1
        elif mes.type == "car_rsu_car":
            network.cntType2 += 1
        else:
            network.cntType3 += 1
        fMessage.write(f"{mes.stt} {mes.indexCar[0]} {mes.startTime} {mes.currentTime} {delay} {mes.type} \n")
    meanDelay = (network.meanDelay + network.countDrop * network.maxDelay) / network.totalOutsize
    fDelay.write(f"{currentTime} \t {meanDelay} \t {network.maxDelay} \t {network.totalOutsize} \t {network.countDrop} \n")
    network.output = []

def dumpOutputFinal(network):
    network.meanDelay = (network.meanDelay + \
            network.countDrop * network.maxDelay) / network.totalOutsize
    f = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.dumpDelayGeneral}", "a")
    f.write(f"{Config.packageStrategy} \t {Config.carAppearStrategy} \t {Config.rsuNumbers} \
              {Config.expName} \t {network.meanDelay} \t {network.countDrop} \t {network.totalOutsize} \
              {network.cntType1} \t {network.cntType2} \t {network.cntType3} \n")
    f.close()
    print("Done dumping final output!!!") 
