from math import *
from numpy import *
from Navigator import Navigator

"""
Author: Sherrie Shen
This code uses the list of pixels returned from Navigator.py and computes the linear and angular velocity.
"""

class Path_To_Velocity:
    def __init__(self, pixel, time_step):
        self.path = pixel
        self.time_step = time_step
        #self.converting_factor = 0.0002645833
        self.converting_factor = 0.05
    def linear_approximation(self, num):
        """
        :param num: number of pixels skipped
        :return: linear approximation of the path with vectors
        """
        vectors_heading = {}
        for i in range(int(len(self.path) / num) - 1):
            x_start = self.path[num * i][0]
            y_start = self.path[num * i][1]
            x_end = self.path[num * (i + 1)][0]
            y_end = self.path[num * (i + 1)][1]
            heading = (x_end - x_start, y_end - y_start)
            vectors_heading[i] = heading
        return vectors_heading

    def get_distance_direction(self, num):
        """
        :param num: number of pixels skipped
        :return: return distance and direction of each vector command
        """
        headings = self.linear_approximation(num)
        distances = {}
        directions = {}
        for i in range(len(headings)):
            x = headings[i][0]
            y = headings[i][1]

            # get distance and direction
            distance = math.sqrt(x ** 2 + y ** 2)
            distances[i] = distance
            direction = (1 / distance * x, 1 / distance * y)
            directions[i] = direction

        return distances, directions

    def get_velocity_commands(self, num):
        """
        :param num: number of pixels skipped
        :return: return a list of commands with angular and linear velocity
        """
        distances, directions = self.get_distance_direction(num)
        commands = []
        old_direction = (1, 0)
        for i in range(len(distances)):
            # find angle to turn
            new_direction = directions[i]
            angle_old_cos = arccos(old_direction[0])
            angle_old_sin = arcsin(old_direction[1])
            if angle_old_sin < 0:  # express angle always in 0 to 2pi
                angle_old = 2 * pi - angle_old_cos
            else:
                angle_old = angle_old_cos
            angle_new_cos = arccos(new_direction[0])
            angle_new_sin = arcsin(new_direction[1])
            if angle_new_sin < 0:
                angle_new = 2 * pi - angle_new_cos
            else:
                angle_new = angle_new_cos
            theta = angle_new - angle_old
            print('theta',theta)

            # calculate linear velocity
            linear_velocity = distances[i] / self.time_step * self.converting_factor

            # calculate angular velocity
            angular_velocity = theta / self.time_step

            # add to commands
            commands.append(angular_velocity)
            commands.append(linear_velocity)

            # update old direction
            old_direction = new_direction

        return commands


if __name__ == '__main__':
    nav = Navigator()
    coordinates = nav.actualAStar((300, 290), (575, 215), "markdown_files/library_lower.png")
    robot = Path_To_Velocity(coordinates, 6)
    robot.get_velocity_commands(10)
