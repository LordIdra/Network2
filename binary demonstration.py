from random import randint, choice
from network2 import *

#TRAINING WILL TAKE FROM 10 MINUTES TO AN HOUR OR MORE DEPENDING ON YOUR COMPUTER

#Now let's run a full test of the network
#We will use a program to generate every possible binary combination using 8 bits and their respective decimal equivalents
#Then we will split this dictionary into 2 parts, training and sample, with a 4:1 ratio
#After training 2-3 hidden layers on the training data we will ask it every training question and take the average
#This should give us a good idea of how good this algorithm is for prediction

#I know there's probably a less stupid looking way to do this(recursion) but I don't want to dive into that right now as it can get complicated quickly
binary = list()
denary = list()

trainingINPUT = list()
testingINPUT = list()

trainingOUTPUT = list()
testingOUTPUT = list()

count = 0

for x1 in range(2):
    for x2 in range(2):
        for x3 in range(2):
            for x4 in range(2):
                for x5 in range(2):
                    for x6 in range(2):
                        for x7 in range(2):
                            for x8 in range(2):
                                binary.append([x1, x2, x3, x4, x5, x6, x7,x8])
                                if count < 10:
                                    countC = str(count) + '0' + '0'
                                elif count < 100:
                                    countC = str(count) + '0'
                                else:
                                    countC = str(count)
                                denary.append(list(countC))
                                denary[-1] = list(map(int, denary[-1]))
                                count += 1

for i in range(int(len(binary)*0.8)):
    selection = randint(0, len(binary)-1)
    trainingINPUT.append(binary[selection])
    trainingOUTPUT.append(denary[selection])
for i in range(int(len(binary)*0.2)):
    selection = randint(0, len(binary)-1)
    testingINPUT.append(binary[selection])
    testingOUTPUT.append(denary[selection])

n = network(8, (40, 40, 40, 40), 3, 0.0002, interface = False)

#Training phase
for x in range(3000):
    index = randint(0, len(trainingINPUT)-1)
    n.setInputs(trainingINPUT[index])
    n.setTargets(trainingOUTPUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()
    
n.addLayer()
for x in range(4000):
    index = randint(0, len(trainingINPUT)-1)
    n.setInputs(trainingINPUT[index])
    n.setTargets(trainingOUTPUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

n.addLayer()
for x in range(5000):
    index = randint(0, len(trainingINPUT)-1)
    n.setInputs(trainingINPUT[index])
    n.setTargets(trainingOUTPUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

n.addLayer()
for x in range(8000):
    index = randint(0, len(trainingINPUT)-1)
    n.setInputs(trainingINPUT[index])
    n.setTargets(trainingOUTPUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()

'''n.addLayer()
for x in range(8000):
    index = randint(0, len(trainingINPUT)-1)
    n.setInputs(trainingINPUT[index])
    n.setTargets(trainingOUTPUT[index])
    n.forwardFeed()
    n.backpropagate()
    n.window.update()'''

#Testing phase
n.interface = True
n.backpropagate()
while True:
    sleep(4)
    index = randint(0, len(testingINPUT)-1)
    n.setInputs(testingINPUT[index])
    n.setTargets(testingOUTPUT[index])
    n.forwardFeed()
    n.window.update()
