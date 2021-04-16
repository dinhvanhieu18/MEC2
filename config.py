class Config:
    # gnb config
    gnbProcessPerSecond = 1280
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = 5
    xList = '150;450;750;1050;1350'
    yList = '1;1;1;1;1'
    zList = '10;10;10;10;10'
    rsuCoverRadius = 151
    rsuProcessPerSecond = 320
    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582
    nActionsRsu = 2
    nStatesRsu = 4

    # car config
    carSpeed = 12
    carCoverRadius = 300
    carProcessPerSecond = 50
    packageStrategy = 'poisson_70'
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582
    nActionsCar = 2
    nStatesCar = 4

    # DQN
    hiddenLayerConfig = [8]
    # policyParamaters = {
    #     "epsilon": 0.5,
    #     "min_epsilon": 0.1,
    #     "epsilon_decay_rate": 0.995
    # }
    queueCapacity = 2000
    batchSize = 16
    learningRate = 0.001
    disCountingFactor = 0.9
    timeToUpdateOnlineModel = 10
    timeToUpdateTargetModel = 50

    # MAB
    learningRateMAB = 0.1
    # policyParamatersMAB = {
    #     "epsilon": 0.5,
    #     "min_epsilon": 0.1,
    #     "epsilon_decay_rate": 0.995
    # }
    policyParamaters = {
        "epsilon": 0.5,
        "w": 250,
    }
    # MAB + DQN
    minprobChooseF = 0.05
    decayRateProbChooseF = 0.95
    threadHoldStable = 0.95

    # message config
    ttl = 5
    maxDelay = 10

    # other
    decayRateMean = 0.8
    maxLenMemory = 100
    fileFolder = "inputFiles"
    carAppearStrategy = 'car_deu5.inp'
    # carPacketStrategy = "poisson_70.inp"
    simTime = 1000
    cycleTime = 0.05
    roadLength = 1500
    loggingFile = "log.log"
    dumpDelayDetail = "delayDetail.txt"
    messageDetail = "messageDetail.txt"
    dumpDelayGeneral = "delayGeneral.txt"
    weightsFolder = "weights"
    resultsFolder = 'results/script1'
    default_pl = 0.5
    default_pr = 0.0
    expName = f"MAB_DQN"
    optimizer = "MAB_DQN"

    
