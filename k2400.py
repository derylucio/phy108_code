import visa
#For more documentattion information
#http://www.av.it.pt/medidas/data/Manuais%20&%20Tutoriais/09%20-%20Power%20Supply%20HP6644/Programming%20Guide.pdf

# initialize k2400.
def init2400(instr):
    rm = visa.ResourceManager()
    k2400 = rm.open_resource(instr)
    # set various k2400 parameters; see k2400 manual for the full selection
    k2400.write('SOUR:VOLT 0') # set voltage to zero
    k2400.write('SOUR:VOLT:RANG 1') # set voltage range
    k2400.write('FORM:ELEM VOLT, CURR') # set communications formatting 
    k2400.write('OUTP ON') # turn on output
    k2400.write('CURR:PROT 100e-3') # set current compliance
    return k2400

# read dc current from k2400
def read2400(k2400):
    return k2400.query_ascii_values("READ?")

# set dc voltage
def set2400(k2400,target_v):
    return k2400.write('SOUR:VOLT %1.6f'%target_v)

def sweep2400(k2400,target_v,step=0.1,delay=0.01):
    cur_v = read2400(k2400)[0]
    while abs(cur_v-target_v) > step:
        if cur_v < target_v:
            set2400(k2400,cur_v+step)
        else:
            set2400(k2400,cur_v-step)
        time.sleep(delay)
        cur_v = read2400(k2400)[0]
    set2400(k2400,target_v)