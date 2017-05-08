from k2400 import *
from tempReader import *
import numpy as np
import time
from tempController import TempPID

#set up readers for thermocouple voltages
#set up power supplies for both blocks
# create the temperature regulator
PWR_ADAPTER = "GPIB0::17::INSTR" # this assumes two different power suplies - need to figure out case of 2 channels of same supply
TEMP_ADAPTERS = ["GPIB0::2::INSTR" , "GPIB0::3::INSTR"]  # this assumes two different readouts - need to figure out case of 2 channels of same readout
TIME_DELAY = 0.1
TEMPERATURES = [2, 5]
POWER_CHANNELS = [1, 2]

#def powerAtTemp(temp):
	# Fill this with Mirae calculations or cooling power 
	# Add a small factor to acount for m*c*delta/time_delay to account for power to heat up reservoir to initial temp.


if __name__ == "__main__":
    powerSupply = init2400(PWR_ADAPTER)
    tempReaders = [initTempReader(adapter) for adapter in TEMP_ADAPTERS]
    temperatures = [readTemp(tempReader) for tempReader in tempReaders] 
    requiredVoltages = [0, 0] #[readTemp(tempReader) for tempReader in tempReaders] # calculate the power required to achive a temperature
    controllers = [TempPID(temp, TIME_DELAY) for temp in TEMPERATURES] # instantiate PID controller  
    while(1):
        for i, channel in enumerate(POWER_CHANNELS):
            target_v = requiredVoltages[i]
            set2400(powerSupply, channel, target_v) # set the voltage to the require voltage 
		
        print requiredVoltages
        time.sleep(TIME_DELAY) # wait for some time 
        temperatures = [readTemp(tempReader) for tempReader in tempReaders] # read the temperature of the ends of the sample
        print temperatures
        diffs = np.abs(np.array(temperatures) - np.array(TEMPERATURES))
        break_out = np.all(diffs < 0.1)
        if break_out : break
		
        for index, temp in enumerate(temperatures):
            pid = controllers[index]
            requiredVoltages[index] = pid.getUpdate(temp) # let the pid tell us what voltage to supply


#TODO: 
# FIGURE OUT TIMESCALES 
# FIGURE OUT ACCCESSING MULTIPLE CHANNELS
