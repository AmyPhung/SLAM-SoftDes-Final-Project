import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np

class OccupancyGrids:
    def __init__(self):
        rospy.init_node('turtlebot_map', anonymous=True)
        rospy.Subscriber('/map', OccupancyGrid, self.map_callback)

    def map_callback(self,data):
        self.map = data

    def get_grid_with_occcupied(self):
        map = self.map
        # build up a numpy array of the coordinates of each grid cell in the map
        Grid = np.zeros((map.info.width * map.info.height, 2))
        total_occupied = 0
        count1 = 0
        for i in range(map.info.width):
            for j in range(map.info.height):
                ind = i + j * map.info.width
                if map.data[ind] > 0:
                    total_occupied += 1
                Grid[count1, 0] = float(i)
                Grid[count1, 1] = float(j)
                count1 += 1

        # build up a numpy array of the coordinates of each occupied grid cell in the map
        Occupied = np.zeros((total_occupied, 2))
        count2 = 0
        for i in range(map.info.width):
            for j in range(map.info.height):
                ind = i + j * map.info.width
                if map.data[ind] > 0:
                    Occupied[count2, 0] = float(i)
                    Occupied[count2, 1] = float(j)
                    count2 += 1
        return Grid, Occupied





if __name__ == '__main__':
    grid = OccupancyGrids()
    Grid, Occupied =grid.get_grid_with_occcupied()
    print(Occupied)
