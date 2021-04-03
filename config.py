class Config:
    # gnb config
    gnbProcessPerSecond = 600
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = 6
    xList = [125, 375, 625, 875, 1125, 1375]
    yList = [1, 1, 1, 1, 1, 1]
    zList = [10, 10, 10, 10, 10, 10]
    rsuCoverRadius = 151
    rsuProcessPerSecond = 320
    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582
    nActionsRsu = 3
    nStatesRsu = 7

    # car config
    carSpeed = 12
    carCoverRadius = 300
    carProcessPerSecond = 50
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582
    nActionsCar = 4
    nStatesCar = 9

    # DQN
    hiddenLayerConfig = [16]
    policyParamaters = {
        "epsilon": 0.5,
        "min_epsilon": 0.1,
        "epsilon_decay_rate": 0.995
    }
    queueCapacity = 2000
    batchSize = 16
    learningRate = 0.001
    disCountingFactor = 0.9
    timeToUpdateOnlineModel = 10
    timeToUpdateTargetModel = 50

    # MAB
    learningRateMAB = 0.1
    policyParamatersMAB = {
        "epsilon": 0.5,
        "min_epsilon": 0.1,
        "epsilon_decay_rate": 0.995
    }
    # MAB + DQN
    probChooseF = 1
    decayRateProbChooseF = 0.995

    # message config
    ttl = 5
    maxDelay = 10

    # other
    decayRateMean = 0.8
    carAppearStrategy = "inputFiles/car_deu20.inp"
    carPacketStrategy = "inputFiles/poisson_50.inp"
    simTime = 1000
    cycleTime = 1.0
    roadLength = 1500
    loggingFile = "log.log"
    dumpDelayDetail = "delayDetail.txt"
    messageDetail = "messageDetail.txt"
    dumpDelayGeneral = "delayGeneral.txt"
    expName = "MAB_DQN"
    weightsFolder = "weights"
    resultsFolder = "results"

    
