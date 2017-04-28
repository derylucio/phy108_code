import visa

def initTempReader(adapter):
	# similar to k2400 code but will need to figure out specifics
	rm = visa.ResourceManager()
    reader = rm.open_resource(instr)
    # set various k2400 parameters; see k2400 manual for the full selection
    reader.write('SOUR:VOLT 0') # set voltage to zero
    reader.write('SOUR:VOLT:RANG 1') # TODO: CONFIRM A VOLTAGE RANGE IN PRACTICE
    reader.write('FORM:ELEM VOLT, CURR') # set communications formatting 
    # reader.write('OUTP ON') => NOT SURE IF THIS IS NEEDED IF WE ARE JUST READING INFO -> CONFIRM
    reader.write('CURR:PROT 100e-3') # set current compliance
    return reader 


def readTemp(instr):
	# Rick says that we can get voltage readings from thermocouple and then convert that to temp. 
	voltage = k2400.query_ascii_values("VOLT?")
	temp =  # TODO: CALCULATE BASED OFF OF REFERENCE INFORMATION FOR THERMOCOUPLE.
	return temp