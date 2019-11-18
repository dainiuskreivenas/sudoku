import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

#import pyNN.spiNNaker as sim
import pyNN.nest as sim

from Sudoku6 import Sudoku6
import logging
from sudoku6_puzzles import puzzles


sim.setup(timestep=2.0,min_delay=2.0,max_delay=2.0, time_scale_factor=40)

logging.info("Setting up the Sudoku Board")

#sudoku6 = Sudoku6(sim, "spinnaker")
sudoku6 = Sudoku6(sim, "nest")

logging.info("Running Simulation")
sudoku6.run(puzzles)


sudoku6.printSpikes()

"""

Single puzzle spikes (useless for more than 1, 
just use print spikes and interpolate results):


print "neurons - {}".format(sudoku6.narc.exe.neuron)
print "synapses - {}".format(sudoku6.narc.exe.connections)

data = {}
def getData(population):
    if population.pop.label in data:
        return data[population.pop.label]
    
    d = population.pop.get_data()
    data[population.pop.label] = d

    return d
    
groups = sudoku6.narc.factGroupRepository.get()
for g in groups:
    for f in groups[g]:
        min = 10000
        pop = sudoku6.narc.exe.getPopulationFromCA(f.caIndex)
        d = getData(pop)
        st = d.segments[0].spiketrains[f.caIndex-pop.fromIndex]
        if len(st) > 0:
            min = st.magnitude[0]
        hasSpiked = len(st) > 0
        print "(f-{} - {} {}) - {} - at {}".format(f.caIndex, f.group, f.attributes, hasSpiked, min)

assertionTimes = {}

neurons = []

for l in sudoku6.rbs.net.assertions:
    neuron = sudoku6.rbs.net.assertions[l]
    neurons.append(neuron)

for n in neurons:
    pop = sudoku6.rbs.get_population(n)
    d = getData(pop)
    index = n - pop.fromIndex

    t = d.segments[0].spiketrains[index]
    if(len(t.magnitude) > 0):
        if (t.magnitude[0] in assertionTimes):
            assertionTimes[t.magnitude[0]] += 1
        else:
            assertionTimes[t.magnitude[0]] = 1

times = []
for t in assertionTimes:
    times.append(t)
    
times.sort()
for t in times:
    print "{} - {}".format(t,assertionTimes[t])
"""

logging.info("End")

sim.end()