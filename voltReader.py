import visa

def initVoltReader(adapter):
    rm = visa.ResourceManager()
    reader = rm.open_resource(adapter)
    return reader 


def readVoltage(instr):
    voltage = instr.query_ascii_values("READ?")
    return voltage[0] 