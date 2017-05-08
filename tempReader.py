import visa

def initTempReader(adapter):
    rm = visa.ResourceManager()
    reader = rm.open_resource(adapter)
    return reader 


def readTemp(instr):
    voltage = instr.query_ascii_values("READ?")
    temp = voltage[0] # TODO: CALCULATE BASED OFF OF REFERENCE INFORMATION FOR THERMOCOUPLE.
    return temp