from PIL import Image, ImageFont, ImageDraw
import textwrap
import numpy as np
import time
import pdb
class Navigator():
    def actualAStar(self,start,finish,map):
        """
        Inputs: starting pixel, finishing pixel, map location
        Outputs: Draws a line of the path the robot needs to take to get to the goalReached.
        currently is still being optimized. It doesn't work excellently as it searches too much.
        """
        sizeOfRobot = 3 # determines the radius of the robot in pixels
        map = Image.open(map) # gets the map image
        x_size = map.size[0] # the x length of the image
        y_size = map.size[1] # the y length of the image
        initialNumber = 10000 # sets the initial values for the Gs, Fs and Hs
        Gs = {} # uses a dictionary to speed up the process
        Hs = {}
        Fs = {}
        obstacles = {}
        for i in range(x_size): # initializes the dictionary of obstacles based on the map.
            for j in range(y_size):
                if(map.getpixel((i,j))[1] < 253):
                    obstacles[(i,j)] = True
        Gs[start] = 0
        pastCoord = start # initializes the starting coordinate
        if (start in obstacles):
            raise ValueError('Starting pixel is an obstacle; it cant be a starting point.')
        if(finish in obstacles):
            raise ValueError('Ending pixel is an obstacle; it cant be an ending point.')
        openList = {}
        closedList = {start:True}
        goalReached = False # a flag to check whether the goal has been reached yet.
        while(not goalReached):
            adjacentCoords = [(pastCoord[0]+1,pastCoord[1]),(pastCoord[0]-1,pastCoord[1]),(pastCoord[0],pastCoord[1]+1),(pastCoord[0],pastCoord[1]-1)] # define the adjacentCoords to check
            for i in adjacentCoords:
                if(not i in closedList):
                    if(i[0] > 0 and i[0] < x_size and i[1] > 0 and i[1] < y_size): # making sure that the bounds aren't out of range.
                        available = self.checkForBorders(i,sizeOfRobot,obstacles)
                        if(available): # if the pixel is allowed, change it's cost
                            Gs[i] = Gs[pastCoord] + 1 # changes the cost
                            Hs[i] = abs(finish[1] - i[1]) + abs(finish[0] - i[0]) # change the h value to be the euclidean distance between the point and the finish
                            Fs[i] = Hs[i] + Gs[i] # the F cost as the sum of the past two
                            openList[i] = Fs[i] # the open list contains the F value to make it easier to pick the lowest f value
                        else:
                            closedList[i] = True # If the pixel is not allowed, it is added to the closed list to prevent further checking.
            if(finish in openList):
                goalReached = True
            min_val = min(openList.itervalues()) # gets the lowest F value in the dictionary of open pixels
            goodKeys = [k for k, v in openList.iteritems() if v == min_val] # gets the pixel(s) with the lowest F value
            HDict = {}
            for i in goodKeys:
                HDict[i] = Hs[i]
            pastCoord = min(HDict, key=HDict.get) # from here, gets the pixel with the lowest H value (most likely to be close to the goal)
            openList.pop(pastCoord)
            closedList[pastCoord] = True
        ListOfCoordinates = self.plotPath(start,finish,Gs,map)
        return ListOfCoordinates
    def plotPath(self,start,finish,Gs,map):
        solution = map
        oldPixel = finish
        ListOfCoordinates = [finish]
        coords = [finish]
        while(start != oldPixel): # while we havn't gotten to the start yet
            coords = [(oldPixel[0]+1,oldPixel[1]),(oldPixel[0]-1,oldPixel[1]),(oldPixel[0],oldPixel[1]+1),(oldPixel[0],oldPixel[1]-1)] # checks the 4 surounding pixels
            Gvalues = [10000,10000,10000,10000] # initializes their values to 0
            for i in range(len(coords)): # puts their values in
                try: # I added a try here bocause it sometimes goes out of bounds, and going out of bounds just means we can't go to that pixel
                    Gvalues[i] = Gs[coords[i]]
                except:
                    Gvalues[i] = 10000
            coordToGoTo = coords[Gvalues.index(min(Gvalues))] # adds the coordinate that we want to go to next.
            ListOfCoordinates = [coordToGoTo] + ListOfCoordinates
            solution.putpixel(coordToGoTo,(0,255,0)) # makes that coordinate red
            oldPixel = coordToGoTo # does it again
        solution.save("Maps/solution.png")
        return ListOfCoordinates
    def checkForBorders(self,i,sizeOfRobot,obstacles):
        """
        Checks the edges of the robot to determine if the pixel in question is a pixel that is allowed to be travelled
        input: i, the coordinate in question, sizeOfRobot, the size of the robot in pixels, obstacles, the coordinates of all the obstacles
        output: boolean, whether the pixel is available or not.
        """
        for j in range(sizeOfRobot): # run through the edges of the square around the robot
            k = 0 # top edge
            if (i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k) in obstacles: # if a pixel on the edge is in the obstacle dictionary
                return False # return False as the pixel is no longer allowed
            k= sizeOfRobot # repeat for bottom edge
            if(i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k) in obstacles:
                return False
        for k in range(sizeOfRobot): # doing the same as above, but for the right and left edges
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
    print("--- %s seconds ---" % (time.time() - start_time))
