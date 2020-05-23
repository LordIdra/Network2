from tkinter import *
from math import sin, pi
from time import sleep

class graph:

    def __init__(self, name, variance, length):

        self.window = Tk()
        self.window.title(name)

        self.c = Canvas(self.window, width = 940, height = 440, bg = 'black')
        self.c.pack()

        self.title = self.c.create_text(500, 24, text = name.upper(), fill = 'red', font = ('', 15))
        self.bottomText = list()

        for i in range(11):
            self.c.create_text(30, ((i+1)*36)+10, text = round(variance-(variance*(i/10)), 2), fill = 'cyan')
        for i in range(11):
            self.c.create_line(53, ((i+1)*36)+10, 893, ((i+1)*36)+10, fill = 'green')

        for i in range(21):
            self.bottomText.append(self.c.create_text(((i+1)*42)+10, 425, text = round(length*(i/20), 2), fill = 'cyan'))
        for i in range(21):
            self.c.create_line(((i+1)*42)+10, 46, ((i+1)*42)+10, 407, fill = 'green')
            
        self.variance = variance
        self.length = length
        self.offset = 0
        self.epochOffset = 0
        
        self.plots = list()
        self.links = list()
        

    def dataShift(self):

        self.offset += ((840)*0.25)
        self.epochOffset += self.length*0.25
        
        for plot in self.plots[0:int((len(self.plots)+1)*0.25)]:
            self.c.delete(plot)
        for link in self.links[0:int((len(self.links)+2)*0.25)]:
            self.c.delete(link)

        self.plots = self.plots[int((len(self.plots)+1)*0.25):len(self.plots)]
        self.links = self.links[int((len(self.links)+2)*0.25):len(self.links)]

        for plot in self.plots:
            self.c.move(plot, -(840*0.25), 0)
        for link in self.links:
            self.c.move(link, -(840*0.25), 0)

        for x in self.bottomText:
            self.c.delete(x)

        for i in range(21):
            self.bottomText.append(self.c.create_text(((i+1)*42)+10, 425, text = round((self.length)*(i/20), 2)+self.epochOffset, fill = 'cyan'))
            

    def plot(self, x, y, link = True):

        if x - self.epochOffset >= self.length:
            self.dataShift()

        x = ((x/self.length)*20)
        y = ((y/self.variance)*10)

        self.plots.append(self.c.create_oval(((x+1)*42)+9-self.offset, (407-((y)*36))-1, ((x+1)*42)+11-self.offset, (407-((y)*36))+1, fill = 'yellow', outline = 'yellow'))
        if link == True:
            try:
                pointsFrom = self.c.coords(self.plots[-2])
                pointsTo = self.c.coords(self.plots[-1])
                self.links.append(self.c.create_line(pointsFrom[0]+1, pointsFrom[1]+1, pointsTo[0]+1, pointsTo[1]+1, fill = 'yellow'))
            except IndexError:
                pass
