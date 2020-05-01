from time import sleep
from random import randint, choice
from tkinter import *
from math import sqrt, exp, pi


#This is our function to convert the numbers into something the neural network can properly understand
#I am using the RELU but other functions include sigmoid, leaky relu and softmax. Each has a different advantage
def rectifyN(x):
    if x < 0:
        return round(0.1*x, 10)
    else:
        return x

#Derivative of the function for backpropagation
def rectifyD(x):
    if x < 0:
        return 0.1
    else:
        return 1

#Convert function for hexidecimal colours(only numerical type that will be accepted by tkinter)
#https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
def convert(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


#Random number generator improvised by me because I tried to learn about bell curve distribution and was immediately swarmed with pages of integrals. Not impressed
#Generate a range which contains all possible random numbers. Some are more common than others (exponentially)
#This is basically, if graphed, a triangle of possible outcomes. The idea is we just return a random number from this range
#DO NOT unless you have a computer stolen from NASA print 'numbers.' it will crash python because the list is so ridiculously huge
#in fact, just the last number 100 is being inserted 100^100 = 10,000 times. there are in total 328,350 items on that list.
numbers = list()
for i in range(100):
    for x in range(i**2):
        numbers.append(i)

def generateNumber():
    x = numbers[randint(0, len(numbers))]/100
    if randint(0, 1) == 0:
        return x
    else:
        return -x


class network:

    #Weight indexing self.weights[layer][from][to]

    def __init__(self, inputNodes, hiddenLayers, outputNodes, lr, interface = True, displayStats = True):

        self.learningRate = lr
        self.epochs = 0
        self.costList = list()
        self.displayStats = displayStats
        
        self.nodes = list()
        self.nodes.append([0 for x in range(inputNodes)])
        self.nodes.append([0 for x in range(hiddenLayers[0])])
        self.nodes.append([0 for x in range(outputNodes)])

        self.sums = self.nodes

        self.targets = [0 for x in range(outputNodes)]
        
        self.hiddenLayers = hiddenLayers
        self.activeLayers = 1

        self.weights = [[], []]

        self.interface = interface

        #Initially I used fully linear random numbers from 0-1 to set the weights
        #However I quickly ran into a problem where upon new weights being initialized, deviation would be so high that all the nodes in the network would die
        #After a bit of research I discovered that using a RNG generator based around a mean and multiplying the result by the root of (2 / number of input nodes)
        #should fix this problem in any scale of network
        
        for x in range(len(self.nodes[0])):
            self.weights[0].append(([generateNumber() * sqrt(2/len(self.nodes[1])) for x in range(len(self.nodes[1]))]))
        for x in range(len(self.nodes[1])):
            self.weights[1].append(([generateNumber() * sqrt(2/len(self.nodes[1])) for x in range(len(self.nodes[2]))]))

        #Interface initialization
        #I will not be using any fullscreen windows for this as to place and configure widgets a lot of division has to be done
        #The computing power needed might be better directed to the algorithm itself in this case
        if interface or displayStats == True:

            totalNodes = list()
            
            totalNodes.append([0 for x in range(inputNodes)]) #Inputs
            for i in range(len(hiddenLayers)):
                totalNodes.append([0 for x in range(hiddenLayers[i])]) #Hidden layers
            totalNodes.append([0 for x in range(outputNodes)]) #Outputs
            totalNodes.append([0 for x in range(outputNodes)]) #Targets

            self.interfaceNodes = list()
            self.interfaceWeights = list()
            self.interfaceTargetLinks = list()

            self.window = Tk()

            self.c = Canvas(self.window, height = 600, width = 1200, bg = 'black')
            self.c.pack()

            verticalDistance = 500/max(len(totalNodes[x]) for x in range(len(totalNodes)))
            horizontalDistance = 1200/len(totalNodes)
            
            for horizontal in range(len(totalNodes)):

                self.interfaceNodes.append(list())

                for vertical in range(len(totalNodes[horizontal])):

                    self.interfaceNodes[horizontal].append(self.c.create_text((horizontal*horizontalDistance)+100, (vertical*verticalDistance)+100, text = '0', fill = 'grey'))

            for x in range(len(self.interfaceNodes[0])):
                self.c.itemconfig(self.interfaceNodes[0][x], fill = 'cyan')
            for x in range(len(self.interfaceNodes[1])):
                self.c.itemconfig(self.interfaceNodes[1][x], fill = 'blue')
            for x in range(len(self.interfaceNodes[-1])):
                self.c.itemconfig(self.interfaceNodes[-1][x], fill = 'purple')
            for x in range(len(self.interfaceNodes[-2])):
                self.c.itemconfig(self.interfaceNodes[-2][x], fill = 'cyan')


            for layer in range(len(totalNodes)-2):

                self.interfaceWeights.append(list()) #layer list

                for fromNode in range(len(totalNodes[layer])):

                    self.interfaceWeights[layer].append(list()) #from-node list

                    x1, y1 = self.c.coords(self.interfaceNodes[layer][fromNode])
                    
                    for toNode in range(len(totalNodes[layer+1])): #to-node list

                        x2, y2 = self.c.coords(self.interfaceNodes[layer+1][toNode])

                        self.interfaceWeights[layer][fromNode].append(self.c.create_line(x1+15, y1, x2-15, y2, fill = 'grey'))

            for output in range(len(totalNodes[-2])):

                x1, y1 = self.c.coords(self.interfaceNodes[-2][output])
                x2, y2 = self.c.coords(self.interfaceNodes[-1][output])
                self.interfaceTargetLinks.append(self.c.create_line(x1+15, y1, x2-15, y2, fill = 'white'))

        if self.displayStats == True:
            self.costText = self.c.create_text(600, 20, fill = 'white', text = 0, font = ('', 20))
            self.epochText = self.c.create_text(400, 20, fill = 'white', text = 0, font = ('', 20))
            self.sampleCostText = self.c.create_text(800, 20, fill = 'white', text = 0, font = ('', 20))

            self.costDESC = self.c.create_text(600, 40, fill = 'red', text = 'CURRENT COST', font = ('', 10))
            self.epochDESC = self.c.create_text(400, 40, fill = 'red', text = 'EPOCHS', font = ('', 10))
            self.sampleDESC = self.c.create_text(800, 40, fill = 'red', text = 'AVERAGE COST', font = ('', 10))


    def addLayer(self):

        if self.activeLayers >= len(self.hiddenLayers):
            pass

        else:

            self.nodes.insert(-1, [0 for x in range(self.hiddenLayers[self.activeLayers-1])])
            self.activeLayers += 1

            newList = list()
            for x in range(len(self.nodes[self.activeLayers])):
                newList.append([generateNumber() * sqrt(2/len(self.nodes[1])) for x in range(len(self.nodes[self.activeLayers]))])

            self.weights.insert(-1, newList)

            for x in self.interfaceNodes[self.activeLayers]:
                self.c.itemconfig(x, fill = 'blue')

            #DESTROY THE FINAL WEIGHT LAYER
            #WITH FIRE
            self.weights[-1] = list()
            for x in range(len(self.nodes[self.activeLayers])):
                self.weights[-1].append(([generateNumber() * sqrt(2/len(self.nodes[self.activeLayers])) for x in range(len(self.nodes[-1]))]))


    def setInputs(self, inputList):
        self.nodes[0] = inputList

    def setTargets(self, targetList):
        self.targets = targetList

        for x in range(len(self.targets)):
            self.c.itemconfig(self.interfaceNodes[-1][x], text = self.targets[x])

    def costIN(self, index): #individual normal
        return float(0.5*((self.nodes[-1][index] - self.targets[index])**2))

    def costFN(self): #full normal
        return float(sum(self.costIN(x) for x in range(len(self.nodes[-1]))) / len(self.nodes[-1]))

    def costID(self, index): #individual derivative
        return float(2*(self.nodes[-1][index] - self.targets[index]))

    def costFD(self): #full derivative
        return float(sum(self.costID(x) for x in range(len(self.nodes[-1]))) / len(self.nodes[-1]))


    def forwardFeed(self):
        
        for layer in range(len(self.nodes)-1):

            for node in range(len(self.nodes[(layer)+1])):

                self.sums[layer+1][node] = round(sum([self.nodes[layer][previousNode] * self.weights[layer][previousNode][node] for previousNode in range(len(self.nodes[layer]))]), 2)

            self.nodes[layer+1] = list(map(rectifyN, self.sums[layer+1]))

        #Interface update
        if self.interface == True:

            for layer in range(self.activeLayers+1):

                for node in range(len(self.nodes[layer])):

                    self.c.itemconfig(self.interfaceNodes[layer][node], text = self.nodes[layer][node])

            for node in range(len(self.nodes[-1])):
                self.c.itemconfig(self.interfaceNodes[-2][node], text = self.nodes[-1][node])


        if self.displayStats == True:
            self.epochs += 1
            self.costList.append(round(self.costFN(), 2))
            if len(self.costList) >= 100:
                self.costList.pop(0)

            average = sum(self.costList) / 100
            
            self.c.itemconfig(self.costText, text = round(self.costFN(), 4))
            self.c.itemconfig(self.epochText, text = round(self.epochs, 4))
            self.c.itemconfig(self.sampleCostText, text = round(average, 4))


    def backpropagate(self):
        #most complex part of the algorithm
        #to fully optimise this we need to take advantage of the chain rule by caching everything that the next calculation set relies on
        #this can actually be looped quite nicely but it is absolute hell to work out
        #we also have to work from the back(negative indexes) which complicates things a bit more

        #first thing we do is get df/dx of our cost function, which gives us our first activation slope
        slopes = list()
        slopes.append([])

        for node in range(len(self.nodes[-1])):

            slopes[0].append(self.costID(node))
        
        for layer in range(len(self.nodes)-1):
            
            slopes.append([])
            
            for fromNode in range(len(self.weights[-(layer+1)])):

                slopes[-1].append(0)

                for toNode in range(len(self.weights[-(layer+1)][fromNode])):

                    cache = slopes[layer][toNode] * rectifyD(self.sums[-(layer+1)][toNode])

                    self.weights[-(layer+1)][fromNode][toNode] -= cache * self.nodes[-(layer+2)][fromNode] * self.learningRate

                    slopes[-1][-1] += cache * self.weights[-(layer+1)][fromNode][toNode]


        for layer in range(len(self.weights)):
            for fromNode in range(len(self.weights[layer])):
                for toNode in range(len(self.weights[layer][fromNode])):
                    self.weights[layer][fromNode][toNode] = round(self.weights[layer][fromNode][toNode], 10)
                    
        #In the writing of the above code, my glasses were thrown across the room only once(totaling twice in the entire programming of this - amazing)
        #Ok, now let's do interface updates
        #These are based on the highest/lowest value in the weights
        if self.interface == True:
            maximiumValue = list()
            for layer in range(len(self.weights)):
                for node in range(len(self.weights[layer])):
                    maximiumValue.append(max(self.weights[layer][node]))
                    maximiumValue.append(-min(self.weights[layer][node]))
            maximiumValue = max(maximiumValue)
            colourValue = 255/maximiumValue
                    
            for layer in range(len(self.weights)-1):
                for nodeFrom in range(len(self.weights[layer])):
                    for nodeTo in range(len(self.weights[layer][nodeFrom])):
                        if self.weights[layer][nodeFrom][nodeTo] < 0:
                            self.c.itemconfig(self.interfaceWeights[layer][nodeFrom][nodeTo], fill = convert(-self.weights[layer][nodeFrom][nodeTo]*colourValue, 0, 0))
                        else:
                            self.c.itemconfig(self.interfaceWeights[layer][nodeFrom][nodeTo], fill = convert(0, self.weights[layer][nodeFrom][nodeTo]*colourValue, 0))
                
            #Weights for final layer
            for nodeFrom in range(len(self.weights[-1])):
                for nodeTo in range(len(self.weights[-1][nodeFrom])):
                    if self.weights[-1][nodeFrom][nodeTo] < 0:
                        self.c.itemconfig(self.interfaceWeights[-1][nodeFrom][nodeTo], fill = convert(-self.weights[-1][nodeFrom][nodeTo]*colourValue, 0, 0))
                    else:
                        self.c.itemconfig(self.interfaceWeights[-1][nodeFrom][nodeTo], fill = convert(0, self.weights[-1][nodeFrom][nodeTo]*colourValue, 0))
