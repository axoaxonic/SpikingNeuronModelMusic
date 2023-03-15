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
        'El': -5.0 * mV,
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
        'El': -10.0 * mV,
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

#G.run_regularly(' = rand()*50*nA, dt=10*ms') # steady current probably instead of random, unless avant guard drum solo is desired
defaultclock.dt = 0.1 * ms
run(2000*ms) # change this for different length tracks

vs = np.clip(statemon[0].v / mV, a_min=None, a_max=0)


print(min(statemon.v[:][0]), max(statemon.v[:][0]))
print(set([int(i) for i in vs]), len(vs))

# clipped version is almost the same, unclipped is 0.80331727 instead of 0; using clipped just in case that number varies with different patterns, 0 is a good constant

# set up pygame mixer and samples

pyg.mixer.init() #if there's lag, try pre_init()

kick = pyg.mixer.Sound('samples/808_Kick_Long.wav')
snare = pyg.mixer.Sound('samples/808_Snare_2.wav')
hatp = pyg.mixer.Sound('samples/808_Hat_Pedal.wav')
hatc = pyg.mixer.Sound('samples/808_Hat_Closed.wav')
hato = pyg.mixer.Sound('samples/808_Hat_Open.wav')
conga = pyg.mixer.Sound('samples/808_Conga.wav')
clap = pyg.mixer.Sound('samples/808_Clap.wav')
shake = pyg.mixer.Sound('samples/808_Shaker.wav')
clave = pyg.mixer.Sound('samples/808_Clave.wav')
crash = pyg.mixer.Sound('samples/808_Cymbal.wav')
tomh = pyg.mixer.Sound('samples/808_Tom_Hi.wav')
toml = pyg.mixer.Sound('samples/808_Tom_Low.wav')
tomm = pyg.mixer.Sound('samples/808_Tom_Mid.wav')
cowbl = pyg.mixer.Sound('samples/808_Cowbell.wav')

C1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-C1.wav')
Cs1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-Cs1.wav')
D1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-D1.wav')
Ds1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-Ds1.wav')
E1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-E1.wav')
F1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-F1.wav')
Fs1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-Fs1.wav')
G1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-G1.wav')
Gs1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-Gs1.wav')
A1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-A1.wav')
As1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-As1.wav')
B1 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-B1.wav')
C2 = pyg.mixer.Sound('samples/Casio-VZ-10M-Quickbass-C2.wav')

Sine40 = pyg.mixer.Sound('samples/40hzSine.wav')
Sine42 = pyg.mixer.Sound('samples/42hzSine.wav')
Sine44p5 = pyg.mixer.Sound('samples/44p5Sine.wav')

R808 = [kick, snare, hatp, hatc, hato, tomh, toml, tomm, cowbl, conga, clap, shake, clave, crash]
CQB = [C1, Cs1, D1, Ds1, E1, F1, Fs1, G1, Gs1, A1, As1, B1, C2]
BassSines = [Sine40, Sine42, Sine44p5]

# link play events to spike threshold, or below threshold -- TODO add rest.wav for silence option, unless there's a better way to pause between events, maybe with the time module? pretty sure just adding 'continue' on the for loop would be way faster than a drum sample, and it would sound like just a bunch of drum samples in a row without the spike-pattern info
import random

for i in vs:

    if i > -40:
        random.choice(BassSines).play()
    else:
        random.choice(R808).play()
        random.choice(R808[:3]).play()
        hatc.play()
    time.sleep(0.01)

