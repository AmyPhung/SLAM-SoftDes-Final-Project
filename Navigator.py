from PIL import Image, ImageFont, ImageDraw
import textwrap
import numpy as np
import time
import pdb
class Navigator():
    def StraightLine(self,start,finish, map):
        """
        Inputs: starting pixel, finishing pixel, map location
        Outputs: draws a straight line on the picture from start to finish
        """
        lineWidth = 2
        map = Image.open(map)
        solution = map
        slope = (start[1] - finish[1]) / (start[0] - finish[0])
        b = start[1] - slope * start[0]
        x_size = map.size[0]
        y_size = map.size[1]
        for x in range(x_size):
            for y in range(y_size):
                if(abs(y - (slope * x + b)) < lineWidth and ((x < finish[0] and x > start[0]) or (x < start[0] and x > finish[0]))
                and ((y < finish[1] and y > start[1]) or (y < start[1] and y > finish[1]))):
                    solution.putpixel((x, y),(255, 0, 0))
                if(abs(x - start[0]) < 3 and abs(y - start[1]) < 3):
                    solution.putpixel((x,y),(0,255,0))
                if(abs(x - finish[0]) < 3 and abs(y - finish[1]) < 3):
                    solution.putpixel((x,y),(0,0,255))
        solution.save("Maps/solution.png")

    def Navigation(self,start,finish, map):
        """
        Inputs: starting pixel, finishing pixel, map location
        Outputs: Draws a line of the path the robot needs to take to get to the goal.
        Right now, this is a very bad implementation of a pathfinding algorithm. I originally
        meant it to be A*, but didn't do a very good job. Below is my start to an actual A* algorithm.
        Currently this implementation takes a long time to run.
        """
        sizeOfRobot = 20 # defines the radius of the robot in pixels
        map = Image.open(map) # gets the map image
        solution = map # makes a solution map
        x_size = map.size[0] # the x length of the image
        y_size = map.size[1] # the y length of the image
        initialNumber = 1000 # sets the initial values for the Gs, Fs and Hs
        Gs = [[initialNumber for y in range(y_size)] for x in range(x_size)] # initializes a matrix of Gs for each pixel
        pastCoord = [start] # initializes the starting coordinate
        cost = 0 # initializes the current cost
        while(len(pastCoord)>0): # while there are still coordinates, keep going
            newCoord = [] # initializes the next coordinates to compute
            for i in pastCoord: # looking at each coordinate
                if(i[0]==finish[0] and i[1]==finish[1]): # if the coordinate is the finish, exit the loop. We're done!
                    Gs[i[0]][i[1]] = cost
                    break
                try: # make sure the number is in bounds
                    if(Gs[i[0]][i[1]] == initialNumber): # check to see if the number has been dealt with before
                        available = True # initializing the availability to true
                        for j in range(sizeOfRobot): # run through the edges of the square around the robot
                            k = 0 # top edge
                            try:
                                if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)): # if a pixel on the edge is black
                                    available = False # set available to False as the pixel is no longer allowed
                                    break # exit the for loop
                            except:
                                    print('bounds too high, but its ok')
                            k= sizeOfRobot # bottom edge
                            try:
                                if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)): # if a pixel on the edge is black
                                    available = False # set available to false as the pixel is no longer allowed
                                    break # exit the for loop
                            except:
                                    print('bounds too high, but its ok')
                        if(available): # if it is already not allowed, we can skip this
                            for k in range(sizeOfRobot): # doing the same as above, but for the rigth and left edges
                                j = 0
                                try:
                                    if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)):
                                        available = False
                                        break
                                except:
                                    print('bounds too high, but its ok')
                                j = sizeOfRobot
                                try:
                                    if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)):
                                        available = False
                                        break
                                except:
                                    print('bounds too high, but its ok')
                        if(available): # if the pixel is allowed, change it's cost
                            Gs[i[0]][i[1]] = cost # changes the cost
                            newCoord = newCoord + [(i[0]+1,i[1]),(i[0]-1,i[1]),(i[0],i[1]+1),(i[0],i[1]-1)] # adds the coordinates the surround the previous one to the list to check
                        else:
                            Gs[i[0]][i[1]] = 9999
                except:
                    print("its ok")
            pastCoord = newCoord # adds the new coordinates to the past coordinates to check next
            cost+=1 # add the costs
        oldPixel = finish # starts with the old pixels at the finish
        ListOfCoordinates = [finish]
        coords = [finish]
        while(oldPixel in coords): # while we havn't gotten to the start yet
            coords = [(oldPixel[0]+1,oldPixel[1]),(oldPixel[0]-1,oldPixel[1]),(oldPixel[0],oldPixel[1]+1),(oldPixel[0],oldPixel[1]-1)] # checks the 4 surounding pixels
            Gvalues = [0,0,0,0] # initializes their values to 0
            for i in range(len(coords)): # puts their values in
                Gvalues[i] = Gs[coords[i][0]][coords[i][1]]
            if(sum(Gvalues) < 10): # if the sum of them is less than 10, the start has been reached
                break
            coordToGoTo = coords[Gvalues.index(min(Gvalues))] # adds the coordinate that we want to go to next.
            ListOfCoordinates = [coordToGoTo] + ListOfCoordinates
            solution.putpixel(coordToGoTo,(255,0,0)) # makes that coordinate red
            oldPixel = coordToGoTo # does it again
        solution.save("Maps/solution.png") # saves the solution to a new picture.
        return ListOfCoordinates
    def actualAStar(self,start,finish,map):
        """
        Inputs: starting pixel, finishing pixel, map location
        Outputs: Draws a line of the path the robot needs to take to get to the goal.
        currently is still being optimized. It doesn't work excellently as it searches too much.
        """
        sizeOfRobot = 5
        map = Image.open(map) # gets the map image
        solution = map # makes a solution map
        x_size = map.size[0] # the x length of the image
        y_size = map.size[1] # the y length of the image
        initialNumber = 10000 # sets the initial values for the Gs, Fs and Hs
        #Gs = [[initialNumber for y in range(y_size)] for x in range(x_size)] # initializes a matrix of Gs for each pixel
        #Hs = [[initialNumber for y in range(y_size)] for x in range(x_size)] # initializes a matrix of Gs for each pixel
        #Fs = [[initialNumber for y in range(y_size)] for x in range(x_size)] # initializes a matrix of Gs for each pixel
        Gs = {}
        Hs = {}
        Fs = {}
        obstacles = {}
        for i in range(x_size):
            for j in range(y_size):
                if(map.getpixel((i,j))[1] < 253):
                    obstacles[(i,j)] = True
        Gs[start] = 0
        pastCoord = start # initializes the starting coordinate
        openList = {}
        closedList = {}
        Goal = False
        randomCounter = 0
        while(not Goal):
            adjacentCoords = [(pastCoord[0]+1,pastCoord[1]),(pastCoord[0]-1,pastCoord[1]),(pastCoord[0],pastCoord[1]+1),(pastCoord[0],pastCoord[1]-1)]
            for i in adjacentCoords:
                if(not i in closedList):
                    if(i[0] > 0 and i[0] < x_size and i[1] > 0 and i[1] < y_size):
                        available = self.checkForBorders(i,sizeOfRobot,obstacles)
                        if(available): # if the pixel is allowed, change it's cost
                            Gs[i] = Gs[pastCoord] + 1 # changes the cost
                            Hs[i] = abs(finish[1] - i[1]) + abs(finish[0] - i[0])
                            Fs[i] = Hs[i] + Gs[i]
                            openList[i] = Fs[i]
                        else:
                            closedList[i] = True
            if(finish in openList):
                Goal = True
            min_val = min(openList.itervalues())
            goodKeys = [k for k, v in openList.iteritems() if v == min_val]
            HDict = {}
            for i in goodKeys:
                HDict[i] = Hs[i]
            pastCoord = min(HDict, key=HDict.get)
            openList.pop(pastCoord)
            closedList[pastCoord] = True
        oldPixel = finish # starts with the old pixels at the finish
        ListOfCoordinates = [finish]
        coords = [finish]
        while(oldPixel in coords): # while we havn't gotten to the start yet
            coords = [(oldPixel[0]+1,oldPixel[1]),(oldPixel[0]-1,oldPixel[1]),(oldPixel[0],oldPixel[1]+1),(oldPixel[0],oldPixel[1]-1)] # checks the 4 surounding pixels
            Gvalues = [10000,10000,10000,10000] # initializes their values to 0
            for i in range(len(coords)): # puts their values in
                try:
                    Gvalues[i] = Gs[coords[i]]
                except:
                    Gvalues[i] = 10000
            if(sum(Gvalues) < 20): # if the sum of them is less than 10, the start has been reached
                break
            coordToGoTo = coords[Gvalues.index(min(Gvalues))] # adds the coordinate that we want to go to next.
            ListOfCoordinates = [coordToGoTo] + ListOfCoordinates
            solution.putpixel(coordToGoTo,(0,255,0)) # makes that coordinate red
            oldPixel = coordToGoTo # does it again
        solution.save("Maps/solution.png")
        return ListOfCoordinates
    def checkForBorders(self,i,sizeOfRobot,obstacles):
        for j in range(sizeOfRobot): # run through the edges of the square around the robot
            k = 0 # top edge
            if (i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k) in obstacles: # if a pixel on the edge is black
                return False # set available to False as the pixel is no longer allowed
            k= sizeOfRobot # bottom edge
            if(i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k) in obstacles: # if a pixel on the edge is black
                return False # set available to false as the pixel is no longer allowed
        for k in range(sizeOfRobot): # doing the same as above, but for the rigth and left edges
            j = 0
            if(i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k) in obstacles:
                return False
            j = sizeOfRobot
            if(i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k) in obstacles:
                return False
        return True

if __name__ == '__main__':
    start_time = time.time()
    nav = Navigator()
    coordinates = nav.actualAStar((300,290),(575,215),"Maps/collected_maps_stage/library_lower.png")
    print(coordinates)
    print("--- %s seconds ---" % (time.time() - start_time))
