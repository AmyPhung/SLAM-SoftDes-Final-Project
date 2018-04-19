from math import *

class Path_To_Velocity:
    def __init__(self,pixel,linear_velocity,angular_velocity):
        self.path = pixel
        self.linear_velocity = linear_velocity
        self.angular_velocity = angular_velocity

    def linear_approximation(self,num):
        vectors_heading = {}
        for i in range(int(len(self.path)/num) - 1):
            x_start = self.path[num*i][0]
            y_start = self.path[num*i][1]
            x_end = self.path[num*(i+1)][0]
            y_end = self.path[num*(i+1)][1]
            heading = (x_end - x_start, y_end - y_start)
            vectors_heading[i] = heading
        return vectors_heading


    def get_distance_direction(self):
        headings = self.linear_approximation(5)
        distances = {}
        directions = {}
        for i in range(len(headings)):
            x = headings[i][1]
            y = headings[i][2]
            distance = math.sqrt(x** 2 + y** 2)
            distances[i] = distance
            direction = (1 / distance * x, 1 / distance * y)
            directions[i]= direction
        return distances, directions

    def get_time(self):
        distances, directions = self.get_distance_direction()
        time = {}
        


            



