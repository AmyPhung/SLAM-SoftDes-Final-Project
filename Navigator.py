from PIL import Image, ImageFont, ImageDraw
import textwrap
import numpy as np
import time

def StraightLine(start,finish, map):
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

def Navigation(start,finish, map):
    """
    Inputs: starting pixel, finishing pixel, map location
    Outputs: Draws a line of the path the robot needs to take to get to the goal.
    """
    sizeOfRobot = 10 # defines the radius of the robot in pixels
    map = Image.open(map) # gets the map image
    solution = map # makes a solution map
    x_size = map.size[0] # the x length of the image
    y_size = map.size[1] # the y length of the image
    initialNumber = 10000 # sets the initial values for the Gs, Fs and Hs
    #Fs = [[initialNumber for y in range(y_size)] for x in range(x_size)] # initializes a matrix of Fs for each pixel
    Gs = [[initialNumber for y in range(y_size)] for x in range(x_size)] # initializes a matrix of Gs for each pixel
    #Hs = [[initialNumber for y in range(y_size)] for x in range(x_size)] # initializes a matrix of Hs for each pixel
    pastCoord = [start] # initializes the starting coordinate
    cost = 0 # initializes the current cost
    while(len(pastCoord)>0): # while there are still coordinates, keep going
        newCoord = [] # initializes the next coordinates to compute
        for i in pastCoord: # looking at each coordinate
            if(i[0]==finish[0] and i[1]==finish[1]): # if the coordinate is the finish, exit hte loop. We're done!
                Gs[i[0]][i[1]] = cost
                #Hs[i[0]][i[1]] = abs(finish[0]-i[0]) + abs(finish[1]-i[1])
                #Fs[i[0]][i[1]] = Gs[i[0]][i[1]] + Hs[i[0]][i[1]]
                break
            if(i[0] > 0 and i[0] < x_size and i[1] > 0 and i[1] < y_size): # make sure the number is in bounds
                if(Gs[i[0]][i[1]] == initialNumber): # check to see if the number has been dealt with before
                    available = True # initializing the availability to true
                    for j in range(sizeOfRobot): # run through the edges of the square around the robot
                        k = 0 # top edge
                        if(i[1]+sizeOfRobot/2-k > 0): # make sure the top edge isnt out of bounds
                            if(i[0]+sizeOfRobot/2-j > 0 and i[0]+sizeOfRobot/2-j < x_size): # make sure the bounds aren't out
                                if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)): # if a pixel on the edge is black
                                    available = False # set available to False as the pixel is no longer allowed
                                    break # exit the for loop
                        k= sizeOfRobot # bottom edge
                        if(i[1]+sizeOfRobot/2-k < y_size): # make sure the bottom edge is in bounds
                            if(i[0]+sizeOfRobot/2-j > 0 and i[0]+sizeOfRobot/2-j < x_size): # make sure the left to right is in bounds
                                if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)): # if a pixel on the edge is black
                                    available = False # set available to false as the pixel is no longer allowed
                                    break # exit the for loop
                    if(available): # if it is already not allowed, we can skip this
                        for k in range(sizeOfRobot): # doing the same as above, but for the rigth and left edges
                            j = 0
                            if(i[0]+sizeOfRobot/2-j > 0):
                                if(i[1]+sizeOfRobot/2-k > 0 and i[1]+sizeOfRobot/2-k < y_size):
                                    if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)):
                                        available = False
                                        break
                            j = sizeOfRobot
                            if(i[0]+sizeOfRobot/2-j < x_size):
                                if(i[1]+sizeOfRobot/2-k > 0 and i[1]+sizeOfRobot/2-k < y_size):
                                    if(map.getpixel((i[0]+sizeOfRobot/2-j,i[1]+sizeOfRobot/2-k)) == (0,0,0)):
                                        available = False
                                        break
                    if(available): # if the pixel is allowed, change it's cost
                        Gs[i[0]][i[1]] = cost # changes the cost
                        #Hs[i[0]][i[1]] = abs(finish[0]-i[0]) + abs(finish[1]-i[1])
                        #Fs[i[0]][i[1]] = Gs[i[0]][i[1]] + Hs[i[0]][i[1]]
                        newCoord = newCoord + [(i[0]+1,i[1]),(i[0]-1,i[1]),(i[0],i[1]+1),(i[0],i[1]-1)] # adds the coordinates the surround the previous one to the list to check
                    else:
                        Gs[i[0]][i[1]] = 9999
        pastCoord = newCoord # adds the new coordinates to the past coordinates to check next
        cost+=1 # add the costs
    oldPixel = finish # starts with the old pixels at the finish
    coords = [finish]
    while(oldPixel in coords): # while we havn't gotten to the start yet
        coords = [(oldPixel[0]+1,oldPixel[1]),(oldPixel[0]-1,oldPixel[1]),(oldPixel[0],oldPixel[1]+1),(oldPixel[0],oldPixel[1]-1)] # checks the 4 surounding pixels
        Gvalues = [0,0,0,0] # initializes their values to 0
        for i in range(len(coords)): # puts their values in
            Gvalues[i] = Gs[coords[i][0]][coords[i][1]]
        if(sum(Gvalues) < 10): # if the sum of them is less than 10, the start has been reached
            break
        coordToGoTo = coords[Gvalues.index(min(Gvalues))] # adds the coordinate that we want to go to next.
        solution.putpixel(coordToGoTo,(255,0,0)) # makes that coordinate red
        oldPixel = coordToGoTo # does it again
    solution.save("Maps/solution.png") # saves the solution to a new picture.
if __name__ == '__main__':
    start_time = time.time()
    Navigation((300,300),(600,200),"Maps/MapNon-Fill.png")
    print("--- %s seconds ---" % (time.time() - start_time))
