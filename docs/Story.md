---
---

# Story/Learning Goals

Originally, we all were interested in learning more about SLAM ([Simultaneous Localization and Mapping](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping)) and using [ROS](http://www.ros.org/). While exploring different examples of SLAM during the first phase of project, we realized our constraints in both time and ability to compile a full SLAM package implemented in ROS with the 6 week timeframe. Therefore, we pivoted and decided to focus our project on creating a script which used the navigation algorithm [A star](https://en.wikipedia.org/wiki/A*_search_algorithm) that interfaced with pre-built mapping ([gmapping](http://wiki.ros.org/gmapping)) and simulation packages ([turtlebot_stage](http://wiki.ros.org/turtlebot_stage)). In addition to the map navigation and robot simulation, we also wanted to test our code on a real turtlebot platform to verify that our map and navigation algorithm yielded usable results. Overall, our goals for this project were to implement the A star algorithm in a python script for path planning and be able to utilize different ROS packages for map data collection and robot simulation.
