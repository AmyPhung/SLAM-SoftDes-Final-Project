import rospy
from convert_path_to_velocity import Path_To_Velocity
from geometry_msgs.msg import Vector3, Twist
from Navigator import Navigator

class Turtlebot:
    def __init__(self):
        rospy.init_node('Velocities')
        self.velpub = rospy.Publisher('/cmd_vel_mux/input/navi',Twist,queue_size=10)
    def goForward(self,listOfVelocities):
        for i in range(len(listOfVelocities)):
            print(listOfVelocities[i])
            if(i % 2 == 1):
                output = Twist()
                output.linear = Vector3(listOfVelocities[i] / 4.0,0,0)
                output.angular = Vector3(0,0,0)
                now = rospy.get_time()
                r = rospy.Rate(20)
                while(now + 4.0 > rospy.get_time()) and (not rospy.is_shutdown()):
                    #print(rospy.get_time())
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
                    r = rospy.Rate(20) # 10hz
                    while(now + 2.0 > rospy.get_time()) and (not rospy.is_shutdown()):
                        #print(rospy.get_time())
                        self.velpub.publish(output)
                        r.sleep()
    def Turn(self):
        output = Twist()
        output.linear = Vector3(0,0,0)
        output.angular = Vector3(0,0,1.0)
        self.velpub.publish(output)
        r = rospy.Rate(10)
        r.sleep()
        now = rospy.get_time()
        while(now + 6.28 > rospy.get_time()) and (not rospy.is_shutdown()):
            #print(rospy.get_time())
            self.velpub.publish(output)
            r.sleep()
        output = Twist()
        output.linear = Vector3(0,0,0)
        output.angular = Vector3(0,0,0)
        self.velpub.publish(output)
if __name__ == '__main__':
    turtle1 = Turtlebot()
    nav = Navigator()
    coordinates = nav.actualAStar((500,1050),(434,918),"Maps/collected_maps_stage/cc3.png")
    print(coordinates)
    Converter = Path_To_Velocity(coordinates,1)
    commands = Converter.get_velocity_commands(10)
    print(commands)
    turtle1.goForward(commands)
