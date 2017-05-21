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
TEMPERATURES = [2, 5]
POWER_CHANNELS = [1, 2]
TODAY = date.today()
OUTPUT_FILE = 'seebeck_out_T1_' + str(TEMPERATURES[0]) + "_T2_" + str(TEMPERATURES[1])  + \
                "_D_" + str(TODAY.year) + "-" + str(TODAY.month)  + "-" +str(TODAY.day)

if __name__ == "__main__":
    run = 1 # change this if we run multiple times in a day
    OUTPUT_FILE += "_" + str(run)
    with open(OUTPUT_FILE, "w+") as output_file:
        # INIT
        powerSupply = init2400(PWR_ADAPTER)
        tempReaders = [initTempReader(adapter) for adapter in TEMP_ADAPTERS]
        temperatures = [readTemp(tempReader) for tempReader in tempReaders] 
        seebeckVoltageReader = initVoltReader(SEEBECK_VOLT_ADAPTER)
        requiredVoltages = [0, 0] 
        controllers = [TempPID(temp, TIME_DELAY) for temp in TEMPERATURES]
        output_file.write(",".join(["T1", "T2", "SEEBECK_VOLTAGE"]) + "\n")
        while(1):
            for i, channel in enumerate(POWER_CHANNELS):
                target_v = requiredVoltages[i]
                set2400(powerSupply, channel, target_v) # set the voltage to the require voltage 
    		
            time.sleep(TIME_DELAY) # wait for some time 
            temperatures = [readTemp(tempReader) for tempReader in tempReaders] # read the temperature of the ends of the sample
            print 'Voltages to supply : ', requiredVoltages
            print 'Current temperatures : ', temperatures
            diffs = np.abs(np.array(temperatures) - np.array(TEMPERATURES))
            at_equilibrium = np.all(diffs < 0.1)
            if at_equilibrium : 
                print 'Equilibrium Attained !'

                seebeck_voltage = readVoltage(seebeckVoltageReader)
                out = str(temperatures[0]) + "," + str(temperatures[1]) + "," + str(seebeck_voltage) + "\n"
                output_file.write(out)
    		
            for index, temp in enumerate(temperatures):
                pid = controllers[index]
                requiredVoltages[index] = pid.getUpdate(temp) # let the pid tell us what voltage to supply

