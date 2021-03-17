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
    policyParamatersRsu = {"epsilon": 0.1}
    hiddenLayerConfigRsu = [16,8]
    queueCapacityRsu = 2000
    batchSizeRsu = 16
    learningRateRsu = 0.001
    disCountingFactorRsu = 0.9
    timeToUpdateTargetModelRsu = 100

    # car config
    carSpeed = 12
    carCoverRadius = 70
    carProcessPerSecond = 100
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582

    nActionsCar = 4
    nStatesCar = 11
    policyParamatersCar = {"epsilon": 0.1}
    hiddenLayerConfigCar = [16,8]
    queueCapacityCar = 2000
    batchSizeCar = 16
    learningRateCar = 0.001
    disCountingFactorCar = 0.9
    timeToUpdateTargetModelCar = 100

    # message config
    ttl = 5

    # other
    carAppearStrategy = "/home/hieu/Desktop/20202/MEC2/inputFiles/car_deu5.inp"
    carPacketStrategy = "/home/hieu/Desktop/20202/MEC2/inputFiles/poisson_70.inp"
    simTime = 30
    cycleTime = 1.0
    roadLength = 1500
    dumpDelayDetail = "/home/hieu/Desktop/20202/MEC2/result/delayDetail.txt"
    dumDelayGeneral = "/home/hieu/Desktop/20202/MEC2/result/delayGeneral.txt"
    weightsDir = "/home/hieu/Desktop/2020/MEC2/weights"
