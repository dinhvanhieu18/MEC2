from config import Config
import os

def dumpOutputPerCycle(network, currentTime):
    if not network.output:
        return
    network.totalOutsize += len(network.output)
    f = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.dumpDelayDetail}", "w")
    for mes in network.output:
        delay = mes.currentTime - mes.sendTime[0]
        network.maxDelay = max(delay, network.maxDelay)
        if mes.isDrop:
            network.countDrop += 1
        else:
            network.meanDelay += delay
        mes.setType()
        f.write(f"{mes.sendTime[0]} \t {mes.currentTime} \t {delay} \t {mes.type} \t {network.maxDelay} \n")
    network.output = []

def dumpOutputFinal(network):
    network.meanDelay = (network.meanDelay + \
            network.countDrop * network.maxDelay) / network.totalOutsize
    f = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.dumpDelayGeneral}", "a")
    f.write(f"{Config.carPacketStrategy} \t {Config.carAppearStrategy} \t \
        {Config.rsuNumbers} \t {network.meanDelay} \t {network.countDrop} \t \
        {network.totalOutsize} \n")
    f.close()
    print("Done dumping final output!!!") 
