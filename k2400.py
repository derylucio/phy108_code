import visa
#For more documentattion information
#http://www.av.it.pt/medidas/data/Manuais%20&%20Tutoriais/09%20-%20Power%20Supply%20HP6644/Programming%20Guide.pdf

# initialize k2400.
def init2400(instr):
    rm = visa.ResourceManager()
    k2400 = rm.open_resource(instr)
    return k2400

# read dc current from k2400
def read2400(k2400, aux_chan):
    query_string = "AUXV?" + str(aux_chan)
    result = k2400.query_ascii_values(query_string)
    return result[0]

# set dc voltage
def set2400(k2400, aux_chan, target_v):
    cmd_string = "AUXV " + str(aux_chan) +  "," + str(target_v)
    return k2400.write(cmd_string)
