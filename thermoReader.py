import visa

def initThermoReader(adapter):
    rm = visa.ResourceManager()
    reader = rm.open_resource(adapter)
    return reader 
	
	# NEED TO PUT IN THE ACTUAL COMMAND:
def readThermo(instr, q_str="KRDG?"):
    voltage = instr.query_ascii_values(q_str)
    temp = voltage[0] # TODO: CALCULATE BASED OFF OF REFERENCE INFORMATION FOR THERMOCOUPLE.
    return temp