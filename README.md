# SLAM Project

This project allows a user to specify a starting point and end goal in a given map and computes a path to navigate a Turtlebot along the path. The maps are generated beforehand with SLAM using Ros package gmapping and odometery data collected from a Turtlebot.

## Getting Started

Clone the repository

```
$ git clone https://github.com/AmyPhung/SLAM-SoftDes-Final-Project.git
```

### Prerequisites
* [Python3](https://stackoverflow.com/questions/42662104/how-to-install-pip-for-python-3-6-on-ubuntu-16-10)
* [Ros kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)
* [Nav2D](http://wiki.ros.org/nav2d)
* [Pillow](https://pillow.readthedocs.io/en/4.0.x/reference/Image.html) - The Image Processing Used


Gmapping - for SLAM

```
$ sudo apt-get install ros-kinetic-slam-gmapping
```

Pillow - change the images
```
$ pip3 install Pillow
```

### Installing

#### Install nav2d for path finding:

```
$ sudo apt-get install ros-kinetic-nav2d
```
#### Install packages for collecting data with Turtlebot2:

Move ```/turtlebot_apps``` and ```/openni_camera``` in your ```~/catkin_ws/src```. Then ```catkin_make``` and ```source ~/.bashrc```.

To teleoperate the Turtlebot2 from your work station, install ssh server on your robot machine

```
sudo apt-get install openssh-server
```

### Running the code
#### Simulation
First, make sure you have the `nav2d_tutorials` package installed.
Put the `start_sim.launch` file in the folder that contains the launch files
(usually in `/opt/ros/kinetic/share/nav2d_tutorials/launch`)
Put the `MapNon-Fill.png`, `start_sim.yaml` and `start_sim.world` files in the world files folder (typically `/opt/ros/kinetic/share/nav2d_tutorials/world`)

To start simulation, use the command
```
roslaunch nav2d_tutorials start_sim.launch
```

To change map change the .png file (making sure to not change the file name)

To move the robot in simulation run PublisherTest.py
```
python3 PublisherTest.py
```
#### Pathfinder
Make sure you have the `pillow` package installed.
To get a picture with a path, run
```
$ python3 Navigator.py
```
There should be a picture named solution.png in maps that looks something like this:
![Path With Solution in Red](/markdown_files/solution.png)
## Examples
#### Build a map with Turtlebot2
To start the robot, on the master node (the robot machine) run the following commands, on three terminals:
```
roscore
roslaunch turtlebot_bringup minimal.launch
roslaunch turtlebot_navigation gmapping_demo.launch

```
To drive the robot from your workstation, on your workstation (the host node), run the following commands:

```
roslaunch turtlebot_rviz_launchers view_navigation.launch
roslaunch turtlebot_teleop keyboard_teleop.launch
```
Save the built map you just created by running the following command on your robot machine:
```
rosrun map_server map_saver -f /tmp/map
```
For troubleshooting and a detailed tutorial of building the map, consult [Gaitech Turtlebot tutorial](http://edu.gaitech.hk/turtlebot/map-navigation.html).
#### Nav2D
Run the following commands on two separate terminals:
```
roslaunch nav2d_tutorial tutorial2.launch
```
On the RViz window, Click on 2D Nav Goal and click somewhere in the map to direct the robot to that spot.
## Authors

* **Amy Phung**
* **Nathan Estill**
* **Sherrie Shen**

## License

This project is licensed under the SAN License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Gaitech Turtlebot Tutorial](http://edu.gaitech.hk/turtlebot/create-map-kenict.html)
* Nav_2D
* hector_slam
