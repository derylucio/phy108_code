def initThermoReader(adapter):
    rm = visa.ResourceManager()
    reader = rm.open_resource(adapter)
    return reader 
	
	# NEED TO PUT IN THE ACTUAL COMMAND:
def readThermo(instr):
    voltage = instr.query_ascii_values("READ?")
    temp = voltage[0] # TODO: CALCULATE BASED OFF OF REFERENCE INFORMATION FOR THERMOCOUPLE.
    return temp