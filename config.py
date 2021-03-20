class Config:
    # gnb config
    gnbProcessPerSecond = 1280
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
    nStatesRsu = 8

    # car config
    carSpeed = 12
    carCoverRadius = 75
    carProcessPerSecond = 100
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582
    nActionsCar = 4
    nStatesCar = 11

    # DQN
    hiddenLayerConfig = [16, 8]
    policyParamaters = {"epsilon": 0.1}
    queueCapacity = 2000
    batchSize = 16
    learningRate = 0.001
    disCountingFactor = 0.9
    timeToUpdateOnlineModel = 10
    timeToUpdateTargetModel = 100

    # message config
    ttl = 5
    maxDelay = 10

    # other
    carAppearStrategy = "inputFiles/car_deu6.inp"
    carPacketStrategy = "inputFiles/poisson_70.inp"
    simTime = 30
    cycleTime = 1.0
    roadLength = 1500
    dumpDelayDetail = "delayDetail.txt"
    dumpDelayGeneral = "delayGeneral.txt"
    weightsFolder = "weights"
    resultsFolder = "results"
