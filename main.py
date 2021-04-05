import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from network import Network
from carSimulator import CarSimulator
from rsuSimulator import RsuSimulator
from gnbSimulator import GnbSimulator
from optimizers.DQN import DQN
from optimizers.MAB import MAB
from optimizers.MAB_DQN import MAB_DQN
from config import Config
from datetime import datetime
import argparse

def main():
    gnb = GnbSimulator()
    rsuList= getRsuList()
    print(len(rsuList))
    carList = carAppear()
    print(len(carList))
    # listTimeMessages = prepareTimeMessages()
    # print(len(listTimeMessages))
    network = Network(
        gnb=gnb,
        rsuList=rsuList,
        carList=carList,
        # listTimeMessages=listTimeMessages,
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
            optimizer=getOptimizer(
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
            optimizer=getOptimizer(
                agent_name=f"car_{index}",
                n_states=Config.nStatesCar,
                n_actions=Config.nActionsCar,
            )
        )
        res.append(car)
        index += 1
        currentTime = timeStartCar
    return res

def getOptimizer(agent_name, n_states, n_actions):
    if Config.optimizer == "MAB":
        optimizer = MAB(
            agent_name=agent_name, 
            n_states=n_states, 
            n_actions=n_actions,
        )
    elif Config.optimizer == "DQN":
        optimizer = DQN(
            agent_name=agent_name, 
            n_states=n_states, 
            n_actions=n_actions,
        )
    elif Config.optimizer == "MAB_DQN":
        optimizer = MAB_DQN(
            agent_name=agent_name, 
            n_states=n_states, 
            n_actions=n_actions,
        )
    else:
        optimizer = None
    return optimizer

def getArgs():
    """
    Get config

    """
    # Get config path from user
    parser = argparse.ArgumentParser()
    parser.add_argument("--pl")
    parser.add_argument("--pr")
    args = parser.parse_args()
    return args

if __name__=="__main__":
    start = datetime.now()
    args = getArgs()
    Config.default_pl = float(args.pl)
    Config.default_pr = float(args.pr)
    Config.expName = f"{args.pl}_{args.pr}"

    if not os.path.exists(f"{os.getcwd()}/{Config.weightsFolder}"):
        os.mkdir(f"{os.getcwd()}/{Config.weightsFolder}")
    if not os.path.exists(f"{os.getcwd()}/{Config.weightsFolder}/{Config.expName}"):
        os.mkdir(f"{os.getcwd()}/{Config.weightsFolder}/{Config.expName}")

    if not os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}"):
        os.mkdir(f"{os.getcwd()}/{Config.resultsFolder}")

    if not os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}"):
        os.mkdir(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}")
    else:
        if os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.messageDetail}"):
            os.remove(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.messageDetail}")
        if os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.loggingFile}"):
            os.remove(f"{os.getcwd()}/{Config.resultsFolder}/{Config.expName}/{Config.loggingFile}")
    main()
    end = datetime.now()
    print(start)
    print(end)
