# Architecture Diagram
### Turtlebot mapping
Use gmapping ROS package to use turtlebot to create a map
### A star algorithm to make a path from a start and end point
Find the shortest path through the generated map
### Convert path to velocity and heading
Convert the path to a set of velocity and heading commands
### Convert velocity and heading to appropriate ROS message types
Convert commands to Twist geometry messages
### Publish ROS commands to appropriate node (either real robot or simulation)
Publish ROS Twist commands to rostopics to control simulated and real robot 
