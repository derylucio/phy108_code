# from k2400 import *
# from tempReader import *
# from voltReader import *
# import numpy as np
# import time
# from tempController import TempPID
from datetime import date

#set up readers for thermocouple voltages
#set up power supplies for both blocks
# create the temperature regulator
PWR_ADAPTER = "GPIB0::17::INSTR" # this assumes two different power suplies - need to figure out case of 2 channels of same supply
SEEBECK_VOLT_ADAPTER = "GPIB0::17::INSTR"
TEMP_ADAPTERS = ["GPIB0::2::INSTR" , "GPIB0::3::INSTR"]  # this assumes two different readouts - need to figure out case of 2 channels of same readout
TIME_DELAY = 0.1
TEMPERATURES = [[2, 5], [5, 8]]
POWER_CHANNELS = [1, 2]
MAX_DATA_POINTS = 1000

dirname = os.getcwd()
OUTPUT_FILE = dirname + "seebeck_out_" + strftime("%Y-%m-%d %H-%M-%S", gmtime()) + ".txt"

if __name__ == "__main__":

    powerSupply = init2400(PWR_ADAPTER)
    tempReaders = [initTempReader(adapter) for adapter in TEMP_ADAPTERS]
    temperatures = [readTemp(tempReader) for tempReader in tempReaders] 
    seebeckVoltageReader = initVoltReader(SEEBECK_VOLT_ADAPTER)
    requiredVoltages = [0, 0] 
    controllers = [TempPID(temp, TIME_DELAY) for temp in TEMPERATURES[temp_index]]
    datapoints_collected = 0
    writeHeader = True

    while(1):
        for i, channel in enumerate(POWER_CHANNELS):
            target_v = requiredVoltages[i]
            set2400(powerSupply, channel, target_v) # set the voltage to the require voltage 
		

        time.sleep(TIME_DELAY) # wait for some time 
        temperatures = [readTemp(tempReader) for tempReader in tempReaders] # read the temperature of the ends of the sample
        print 'Voltages to supply : ', requiredVoltages
        print 'Current temperatures : ', temperatures
        diffs = np.abs(np.array(temperatures) - np.array(TEMPERATURES[temp_index]))
        at_equilibrium = np.all(diffs < 0.1)

        if at_equilibrium :
            out_loc = OUTPUT_FILE + "_T1_" + str(TEMPERATURES[temp_index][0]) + "_T2_" + str(TEMPERATURES[temp_index][1])
            output_file =  open(out_loc, "w+") 
            if writeHeader : 
                writeHeader = False
                output_file.write(",".join(["T1", "T2", "SEEBECK_VOLTAGE"]) + "\n")

            print 'Equilibrium Attained !'
            seebeck_voltage = readVoltage(seebeckVoltageReader)
            out = str(temperatures[0]) + "," + str(temperatures[1]) + "," + str(seebeck_voltage) + "\n"
            output_file.write(out)
            datapoints_collected += 1
            if datapoints_collected >= MAX_DATA_POINTS:
                datapoints_collected = 0
                temp_index += 1
                writeHeader = True
		
        for index, temp in enumerate(temperatures):
            pid = controllers[index]
            requiredVoltages[index] = pid.getUpdate(temp) # let the pid tell us what voltage to supply

