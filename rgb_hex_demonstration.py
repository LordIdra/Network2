from network2 import *
from random import randint
from tkinter import *
from time import sleep

inputs = []
outputs = []

def check(x):
    return int(x, base = 16)
    
def modconvert(r, g, b):
    x = '%02x%02x%02x' % (int(r), int(g), int(b))
    return x[0:2], x[2:4], x[4:6]

for r in range(16):
    for g in range(16):
        for b in range(16):
            
            if r*17 < 10:
                r1 = '00' + str(r*17)
            elif r*17 < 100:
                r1 = '0' + str(r*17)
            elif r*17 < 1000:
                r1 = str(r*17)

            if g*17 < 10:
                g1 = '00' + str(g*17)
            elif g*17 < 100:
                g1 = '0' + str(g*17)
            elif g*17 < 1000:
                g1 = str(g*17)

            if b*17 < 10:
                b1 = '00' + str(b*17)
            elif b*17 < 100:
                b1 = '0' + str(b*17)
            elif b*17 < 1000:
                b1 = str(b*17)
                
            inputs.append([r1[0], r1[1], r1[2], g1[0], g1[1], g1[2], b1[0], b1[1], b1[2]])
            out1, out2, out3 = modconvert(r*17, g*17, b*17)

            outputs.append([out1[0], out1[1], out2[0], out2[1], out3[0], out3[1]])

            inputs[-1] = list(map(check, inputs[-1]))
            outputs[-1] = list(map(check, outputs[-1]))

testing_input = []
testing_output = []

training_input = []
training_out = []

for x in range(int(len(inputs)/2)):
    index = randint(0, len(inputs)-1)
    training_input.append(inputs[index])
    training_out.append(outputs[index])

for x in range(int(len(inputs)/4)):
    index = randint(0, len(inputs)-1)
    testing_input.append(inputs[index])
    testing_output.append(outputs[index])

n = network(9, [18, 18, 18], 6, 0.000008, forwardGraphHeight = 20)

for i in range(2000):
    index = randint(0, len(training_input)-1)
    n.setInputs(training_input[index])
    n.setTargets(training_out[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

n.addLayer()

for i in range(4000):
    index = randint(0, len(training_input)-1)
    n.setInputs(training_input[index])
    n.setTargets(training_out[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

n.addLayer()

for i in range(6000):
    index = randint(0, len(training_input)-1)
    n.setInputs(training_input[index])
    n.setTargets(training_out[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

while True:
    index = randint(0, len(testing_input)-1)
    n.setInputs(testing_input[index])
    n.setTargets(testing_output[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()
    sleep(2)
