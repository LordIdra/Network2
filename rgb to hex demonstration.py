from network2 import *
from random import randint
from tkinter import *
from time import sleep

inputs = list()
outputs = list()

def check(x):
    if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        pass
    else:
        if x == 'a':
            x = 10
        elif x == 'b':
            x = 11
        elif x == 'c':
            x = 12
        elif x == 'd':
            x = 13
        elif x == 'e':
            x = 14
        elif x == 'f':
            x = 15

    return int(x)
    
def modconvert(r, g, b):
    x = str('%02x%02x%02x' % (int(r), int(g), int(b)))
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

testingIN = list()
testingOUT = list()

trainingIN = list()
trainingOUT = list()

for x in range(int(len(inputs)/2)):
    index = randint(0, len(inputs)-1)
    trainingIN.append(inputs[index])
    trainingOUT.append(outputs[index])

for x in range(int(len(inputs)/4)):
    index = randint(0, len(inputs)-1)
    testingIN.append(inputs[index])
    testingOUT.append(outputs[index])

n = network(9, [18, 18, 18], 6, 0.000008, forwardGraphHeight = 20)

for i in range(2000):
    index = randint(0, len(trainingIN)-1)
    n.setInputs(trainingIN[index])
    n.setTargets(trainingOUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

n.addLayer()

for i in range(4000):
    index = randint(0, len(trainingIN)-1)
    n.setInputs(trainingIN[index])
    n.setTargets(trainingOUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

n.addLayer()

for i in range(6000):
    index = randint(0, len(trainingIN)-1)
    n.setInputs(trainingIN[index])
    n.setTargets(trainingOUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

while True:
    index = randint(0, len(testingIN)-1)
    n.setInputs(testingIN[index])
    n.setTargets(testingOUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()
    sleep(2)
