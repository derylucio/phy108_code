# TODO: PUT IN THE INSTRUMENT THAT READS FROM THE PRE_CALIBRATED THERMOMETER:
# TODO: FIGURE OUT REASONABLE CUTOFF TEMPERATURE FOR RECALIBRATION

# Note, this code currently works under the assumption that the CERNOX thermometer can be treated 
# the same way as the DMMs.  In the case that this isn't true, will need to modify the code. 

# Last Edit: 5/14/17 - 10:15PM Mirae 

# for the timestamp:
from time import gmtime, strftime


#Need to put third instrument into the following list:
TEMP_ADAPTERS = ["GPIB0::2::INSTR" , "GPIB0::3::INSTR"]  
TIME_DELAY = 0.1
OUTPUT_FILE = "tc_calibration_file" + strftime("%Y-%m-%d %H-%M-%S", gmtime()) + ".txt" # puts timestamp on filename

 
if __name__ == "__main__":

	file = open(OUTPUT_FILE, "w+") #if file doesn't already exist, will create it. 
    tempReaders = [initTempReader(adapter) for adapter in TEMP_ADAPTERS]
    temperatures = [readTemp(tempReader) for tempReader in tempReaders] 
	starter_string = "voltage from TC One " + "Voltage from TC Two " + "Temperature from Thermometer "
    file.write(starter_string)
	
	#want to wait until it recalibrates - figure out a reasonable value
    while(temperature[2] < 100):
        time.sleep(TIME_DELAY) # wait for some time 
        temperatures = [readTemp(tempReader) for tempReader in tempReaders] # read the temperatures from all devices
		update_string = str(temperatures[0] + "," + temperatures[1] + "," + temperatures[2])
		file.write(update_string)
	
	file.close()


