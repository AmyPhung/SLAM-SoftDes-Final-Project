
---
---

# Demonstration
We start out by getting the following map from Lidar data from the TurtleBot.

![Example Map of the Library](img/library_lower_day2.png)

Then we select two points in the map that we want the robot to traverse, and our program draws a path on the map using the A* algorithm.

![Path in the Library](img/solution.png)

Then we publish the velocities to ROS, and the robot moves in real life.


Demonstration of paths explored using the A* algorithm:

![Astar Working](img/astar_map.gif)

Video of the robot traveling along a path:

[![Demo](img/TurtlebotDemo.JPG)](https://www.youtube.com/watch?v=fbsQO-QRdyw)
