from brian2 import *
import struct
import numpy as np
# from scipy import signal as sg

# this test code with a single random input current Hodgkin Huxley neuron is copied from an example from the Brian2 documentation

area = 20000*umetre**2
Cm = 1*ufarad*cm**-2 * area
gl = 5e-5*siemens*cm**-2 * area
El = -65*mV
EK = -90*mV
ENa = 50*mV
g_na = 100*msiemens*cm**-2 * area
g_kd = 30*msiemens*cm**-2 * area
VT = -63*mV

eqs_HH = '''
dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt
dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
    (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
    (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
    (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
I : amp
'''
#TODO add izhikevich and other neurons

group = NeuronGroup(1, eqs_HH, threshold='v > -40*mV', refractory='v > -40*mV', method='exponential_euler')

group.v = El
statemon = StateMonitor(group, 'v', record=True)
spikemon = SpikeMonitor(group, variables='v')

group.run_regularly('I = rand()*50*nA', dt=10*ms)
run(5000*ms)

print(min(statemon.v[:][0]), max(statemon.v[:][0]), len(statemon.v[:][0]))

# sample_rate = 44100 # confusingly, the run length of the spiketrain has to become the samples, so the frequency/samplerate method doesn't really work

f = open('HH.wav', 'wb') # can be changed to mp3 without LAME encoding and it still plays

for i in np.array((statemon.v[:][0])):
    f.write(struct.pack('b', int(i+100))) # If it comes out as silence, it might be just too low of frequency to hear

f.close()

