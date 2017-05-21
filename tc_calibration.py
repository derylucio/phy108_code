# TODO: PUT IN THE INSTRUMENT THAT READS FROM THE PRE_CALIBRATED THERMOMETER:
# TODO: FIGURE OUT REASONABLE CUTOFF TEMPERATURE FOR RECALIBRATION

# Note, this code currently works under the assumption that the CERNOX thermometer can be treated 
# the same way as the DMMs.  In the case that this isn't true, will need to modify the code. 

# Last Edit: 5/16/17 - 10:15AM Mirae 

# for the timestamp:
#from time import gmtime, strftime
import time
import os
import visa
from tempReader import *


#Need to put third instrument into the following list:
TEMP_ADAPTERS = [ "GPIB0::2::INSTR", "GPIB0::3::INSTR"] 
CERNOX_ADAPTER = ["GPIB0::30::INSTR"] 
TIME_DELAY = 0.1
dirname = "C:\\Users\\Student\\Desktop\\P108 Users\\ThermoElectric\\phy108_code-master\\TempCalFiles\\"
OUTPUT_FILE = dirname + "tc_calibration_file" + time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime()) + ".txt" # puts timestamp on filename

 
if __name__ == "__main__":

    file = open(OUTPUT_FILE, "w+") #if file doesn't already exist, will create it. 
    tempReaders = [initTempReader(adapter) for adapter in TEMP_ADAPTERS]
    themometers = [initTempReader(adapter) for adapter in CERNOX_ADAPTER]
    temperatures = [readTemp(tempReader) for tempReader in tempReaders] 
    thermotemp = [readTemp(adapter, "KRDG?") for adapter in themometers]
    starter_string = "TC One " + "TC Two " + "Thermometer \n"
    file.write(starter_string)
    while(1):
		if(thermotemp[0] < 280):
			time.sleep(TIME_DELAY)
			temperatures = [readTemp(tempReader) for tempReader in tempReaders]
			thermotemp = [readTemp(adapter, "KRDG?") for adapter in themometers]
			print temperatures, thermotemp
			update_string = str(temperatures[0]) + "," + str(temperatures[1]) + "," + str(thermotemp[0]) + '\n' # ','.join(array)
			file.write(update_string)
	
    file.close()


