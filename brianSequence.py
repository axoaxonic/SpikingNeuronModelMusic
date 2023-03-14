from brian2 import *
import pygame as pyg # oink oink. could use something like playsound but pygame has more options than just 'play wav.' SoLoud is an even more expressive option but requires compiling a C++ program and calling it thru the Python API, and I wanted to make this repo lighter than that.

# Set up the neuron parameters with Brian2

#Cm = 100 * pF
#gl = 12 * nS
#El = -60.0 * mV
#VT = -50.0 * mV
#d_t = 2.0 * mV
#a = -11.0 * nS
#tau = 130.0 * ms
#b = 30.0 * pA
#VR = -48.0 * mV
#I = 160 * pA

patterns = { # from https://brian2.readthedocs.io/en/stable/examples/frompapers.Naud_et_al_2008_adex_firing_patterns.html
    'tonicSpiking': {
        'Cm': 200 * pF,
        'gl': 10 * nS,
        'El': -70.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': 2.0 * nS,
        'tau': 30.0 * ms,
        'b': 0.0 * pA,
        'VR': -58.0 * mV,
        'I': 500 * pA,
    },
    'adaptation': {
        'Cm': 200 * pF,
        'gl': 12 * nS,
        'El': -70.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': 2.0 * nS,
        'tau': 300.0 * ms,
        'b': 60.0 * pA,
        'VR': -58.0 * mV,
        'I': 500 * pA,
    },
    'initialBurst': {
        'Cm': 130 * pF,
        'gl': 18 * nS,
        'El': -58.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': 4.0 * nS,
        'tau': 150.0 * ms,
        'b': 120.0 * pA,
        'VR': -50.0 * mV,
        'I': 400 * pA,
    },
    'regularBursting': {
        'Cm': 200 * pF,
        'gl': 10 * nS,
        'El': -58.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': 2.0 * nS,
        'tau': 120.0 * ms,
        'b': 100.0 * pA,
        'VR': -46.0 * mV,
        'I': 210 * pA,
    },
    'delayedAccelerating': {
        'Cm': 200 * pF,
        'gl': 12 * nS,
        'El': -70.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': -10.0 * nS,
        'tau': 300.0 * ms,
        'b': 0.0 * pA,
        'VR': -58.0 * mV,
        'I': 300 * pA,
    },
    'delayedRegularBursting': {
        'Cm': 100 * pF,
        'gl': 10 * nS,
        'El': -65.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': -10.0 * nS,
        'tau': 90.0 * ms,
        'b': 30.0 * pA,
        'VR': -47.0 * mV,
        'I': 110 * pA,
    },
    'transientSpiking': {
        'Cm': 100 * pF,
        'gl': 10 * nS,
        'El': -65.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': 10.0 * nS,
        'tau': 90.0 * ms,
        'b': 100.0 * pA,
        'VR': -47.0 * mV,
        'I': 180 * pA,
    },
    'irregularSpiking': {
        'Cm': 100 * pF,
        'gl': 12 * nS,
        'El': -60.0 * mV,
        'VT': -50.0 * mV,
        'd_t': 2.0 * mV,
        'a': -11.0 * nS,
        'tau': 130.0 * ms,
        'b': 30.0 * pA,
        'VR': -48.0 * mV,
        'I': 160 * pA,
    },
}

eqs = '''
    dv/dt = (gl*(El - v) + gl*d_t*exp((v-VT)/d_t) + I - w)/Cm : volt
    dw/dt  = (a*(v - El) - w)/tau : amp
'''# ...

G = NeuronGroup(1, eqs, threshold='v > 0*mV', reset='v = VR; w += b', method='euler', namespace=patterns['irregularSpiking']) #change namespace for different patterns in pattern dictionary

G.v = -50*mV # would be better if it grabs the El value from whatever pattern is used in G namespace TODO lookup if NeuronGroup submodule allows to access individual namespace items
G.w = 0

spikemon = SpikeMonitor(G, variables='v')
statemon = StateMonitor(G, ['v', 'w'], record=True, when='thresholds')

#G.run_regularly('I = rand()*50*nA, dt=10*ms') # steady current probably instead of random, unless avant guard drum solo is desired
defaultclock.dt = 0.1 * ms
run(900*ms) # change this for different length tracks

vs = np.clip(statemon[0].v / mV, a_min=None, a_max=0)


print(min(statemon.v[:][0]), max(statemon.v[:][0]))
print(min(vs), max(vs))

# clipped version is almost the same, unclipped is 0.80331727 instead of 0; using clipped just in case that number varies with different patterns, 0 is a good constant

# set up pygame mixer and samples

pyg.mixer.init() #if there's lag, try pre_init()

kick = pyg.mixer.Sound('samples/808_Kick_Short.wav')
snare = pyg.mixer.Sound('samples/808_Snare_2.wav')
hat = pyg.mixer.Sound('samples/808_Hat_Pedal.wav')
conga = pyg.mixer.Sound('samples/808_Conga.wav')
# link play events to spike threshold, or below threshold -- TODO add rest.wav for silence option, unless there's a better way to pause between events, maybe with the time module? pretty sure just adding 'continue' on the for loop would be way faster than a drum sample, and it would sound like just a bunch of drum samples in a row without the spike-pattern info

for i in vs:
    if i < 0:
        kick.play(int())
    elif i == 0:
        conga.play()
        snare.play()
    time.sleep(0.01)
