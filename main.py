from utils import getConfig
from simulator import Simulator

if __name__=="__main__":

    config = getConfig()

    Simulator.gnbProcessPerSecond = config["gnb_process_per_second"]
    Simulator.gnbCarMeanTranfer = config["gnb_car_mean_tranfer"]
    
    Simulator.rsuNumbers = config["rsu_numbers"]
    Simulator.xList = config["list_rsu_xcoord"]
    Simulator.yList = config["list_rsu_ycoord"]
    Simulator.zList = config["list_rsu_zcoord"]
    Simulator.rsuCoverRadius = config["rsu_cover_radius"]
    Simulator.rsuProcessPerSecond = config["rsu_process_per_second"]
    Simulator.rsuRsuMeanTranfer = config["rsu_rsu_mean_tranfer"]
    Simulator.rsuCarMeanTranfer = config["rsu_car_mean_tranfer"]
    Simulator.rsuGnbMeanTranfer = config["rsu_gnb_mean_tranfer"]
    Simulator.pRsuToCar = config["default_p_rsu_to_car"]
    Simulator.pRsuToRsu = config["default_p_rsu_to_rsu"]
    Simulator.pRsuToGnb = config["default_p_rsu_to_gnb"]
    
    Simulator.carSpeed = config["car_speed"]
    Simulator.carCoverRadius = config["car_cover_radius"]
    Simulator.carProcessPerSecond = config["car_process_per_second"]
    Simulator.carCarMeanTranfer = config["car_car_mean_tranfer"]
    Simulator.carRsuMeanTranfer = config["car_rsu_mean_tranfer"]
    Simulator.carGnbMeanTranfer = config["car_gnb_mean_tranfer"]
    Simulator.pCarToCar = config["default_p_car_to_car"]
    Simulator.pCarToRsu = config["default_p_car_to_rsu"]
    Simulator.pCarToGnb = config["default_p_car_to_gnb"]
    
    Simulator.carAppearStrategy = config["car_appear_strategy"]
    Simulator.carPacketStrategy = config["car_packet_strategy"]
    Simulator.simTime = config["sim_time"]
    Simulator.cycleTime = config["cycle_time"]
    Simulator.roadLength = config["road_length"]
    Simulator.dumpDelayDetail = config["dump_delay_detail"]
    Simulator.dumDelayGeneral = config["dump_delay_general"]

    Simulator.main()
