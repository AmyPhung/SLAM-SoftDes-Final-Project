import rospy
from convert_path_to_velocity import Path_To_Velocity
from geometry_msgs.msg import Vector3, Twist
from Navigator import Navigator

class Turtlebot:
    def __init__(self):
        rospy.init_node('Velocities')
        self.velpub = rospy.Publisher('/cmd_vel_mux/input/navi',Twist,queue_size=10)
    def publishVelocities(self,listOfVelocities):
        """
        Input: takes a list of Velocities, alternating angular and linear.
        Output: publishes velocities for a certain amount of time to the rostopic
        """
        r = rospy.Rate(20)
        r.sleep()
        for i in range(len(listOfVelocities)):
            print(listOfVelocities[i])
            if(i % 2 == 1):
                output = Twist()
                output.linear = Vector3(listOfVelocities[i] / 4.0,0,0)
                output.angular = Vector3(0,0,0)
                now = rospy.get_time()
                while(now + 4.0 > rospy.get_time()) and (not rospy.is_shutdown()):
                    self.velpub.publish(output)
                    r.sleep()
            else:
                if(listOfVelocities[i] != 0):
                    output = Twist()
                    if(listOfVelocities[i] > 3.14):
                        listOfVelocities[i] = listOfVelocities[i] - 6.28
                    output.linear = Vector3(0,0,0)
                    output.angular = Vector3(0,0,-listOfVelocities[i] / 2.0)
                    now = rospy.get_time()
                    while(now + 2.0 > rospy.get_time()) and (not rospy.is_shutdown()):
                        self.velpub.publish(output)
                        r.sleep()
    def Turn(self):
        """
        For testing the turning of the robot, not actually used.
        Turns the robot one full rotation.
        """
        output = Twist()
        output.linear = Vector3(0,0,0)
        output.angular = Vector3(0,0,1.0)
        self.velpub.publish(output)
        r = rospy.Rate(10)
        r.sleep()
        now = rospy.get_time()
        while(now + 6.28 > rospy.get_time()) and (not rospy.is_shutdown()):
            self.velpub.publish(output)
            r.sleep()
        output = Twist()
        output.linear = Vector3(0,0,0)
        output.angular = Vector3(0,0,0)
        self.velpub.publish(output)
if __name__ == '__main__':
    nav = Navigator()
    coordinates = nav.actualAStar((500,1050),(434,918),"Maps/collected_maps_stage/cc3.png") # get the path
    Converter = Path_To_Velocity(coordinates,1)
    commands = Converter.get_velocity_commands(10) # convert the path to velocities
    turtle1 = Turtlebot()
    turtle1.publishVelocities(commands) # publish the velocities to the robot.
