from network2 import *
from random import randint
from math import pi
from time import sleep

n = network(1, [3], 1, 0.0001, interface = True)

piset_in = list()
piset_out = list()

for i in range(20):
    piset_in.append(i)
    piset_out.append(2*i*pi)

training_in = piset_in[0:14]
training_out = piset_out[0:14]

testing_in = piset_in[14:19]
testing_out = piset_out[14:19]

for i in range(2000):
    AN_IDIOTIC_VARIABLE = randint(0, len(training_in)-1)
    n.setInputs([training_in[AN_IDIOTIC_VARIABLE]])
    n.setTargets([training_out[AN_IDIOTIC_VARIABLE]])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()
    sleep(0.01)
    
while True:
    AN_IDIOTIC_VARIABLE = randint(0, len(testing_in)-1)
    n.setInputs([testing_in[AN_IDIOTIC_VARIABLE]])
    n.setTargets([testing_out[AN_IDIOTIC_VARIABLE]])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()
    sleep(2)
