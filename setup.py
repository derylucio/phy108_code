from k2400 import *
from tempReader import *
import numpy as np
import time
from tempController import TempPID

#set up readers for thermocouple voltages
#set up power supplies for both blocks
# create the temperature regulator
PWR_ADAPTERS = ["GPIB::1" , "GPIB::12"] # this assumes two different power suplies - need to figure out case of 2 channels of same supply
TEMP_ADAPTERS = ["GPIB::8" , "GPIB::1"]  # this assumes two different readouts - need to figure out case of 2 channels of same readout
TIME_DELAY = 0.1
WIRE_RESISTANCE = 10e2
TEMPERATURES = [90, 95]

def powerAtTemp(temp):
	# Fill this with Mirae calculations or cooling power 
	# Add a small factor to acount for m*c*delta/time_delay to account for power to heat up reservoir to initial temp.


if __name__ == "__main__":
	powerSupplies = [init2400(adapter) for adapter in PWR_ADAPTERS] # instantiate power supplies 
	requiredVoltages = [np.sqrt(powerAtTemp(temp)*WIRE_RESISTANCE) for temp in TEMPERATURES]  # calculate the power required to achive a temperature
	tempReaders = [initTempReader(adapter) for adapter in TEMP_ADAPTERS]
	controllers = [TempPID(temp, TIME_DELAY) for temp in TEMPERATURES] # instantiate PID controller  
	while(1):
		for i, supply in enumerate(powerSupplies):
			set2400(supply, requiredVoltages[i]) # set the voltage to the require voltage 
			time.sleep(TIME_DELAY) # wait for some time 
			temperatures = [readTemp(tempReader) for tempReader in tempReaders] # read the temperature of the ends of the sample
			for index, temp in enumerate(temperatures):
				pid = controller[index]
				requiredVoltages[index] = pid.getUpdate(temp) # let the pid tell us what voltage to supply



#TODO: 
# FIGURE OUT TIMESCALES 
# FIGURE OUT ACCCESSING MULTIPLE CHANNELS
