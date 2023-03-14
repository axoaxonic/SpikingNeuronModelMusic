from brian2 import *
import pygame as pyg # oink oink. could use something like playsound but pygame has more options than just "play wav." SoLoud is an even more expressive option but requires compiling a C++ program and calling it thru the Python API, and I wanted to make this repo lighter than that.

# Set up the neuron parameters with Brian2

area = 20000*umetre**2
Cm = 1*ufarad*cm**-2 * area
gl = 5e-5*siemens*cm**-2 * area
El = -65*mV
EK = -90*mV #TODO change synthesis file from Ek to EK
ENa = 50*mV
g_na = 100*msiemens*cm**-2 * area
g_kd = 30*msiemens*cm++-2 * area
VT = -63*mV

eqs_ # ...

group = NeuronGroup(1, eqs_, threshold='v > -40*mV', refractory='v > -40*mV', method='rk2')

spikemon = SpikeMonitor()
statemon = StateMonitor()

# set up pygame mixer and samples

pyg.mixer.init() #if there's lag, try pre_init()

kick = pyg.mixer.Sound('./samples/808_Kick_Short.wav')
snare = pyg.mixer.Sound('./samples/808_Snare_2.wav')

# link play events to spike threshold, or below threshold -- TODO add rest.wav for silence option, unless there's a better way to pause between events, maybe with the time module? pretty sure just adding "continue" on the for loop would be way faster than a drum sample, and it would sound like just a bunch of drum samples in a row without the spike-pattern info


