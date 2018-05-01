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
                output.linear = Vector3(listOfVelocities[i],0,0)
                output.angular = Vector3(0,0,0)
                now = rospy.get_time()
                r = rospy.Rate(10)
                while(now + 1.0 > rospy.get_time()) and (not rospy.is_shutdown()):
                    #print(rospy.get_time())
                    self.velpub.publish(output)
                    r.sleep()
            else:
                output = Twist()
                output.linear = Vector3(0,0,0)
                if(i == 0):
                    output.angular = Vector3(0,0,-listOfVelocities[i])
                else:
                    output.angular = Vector3(0,0,listOfVelocities[i])
                now = rospy.get_time()
                r = rospy.Rate(20) # 10hz
                while(now + 1.0 > rospy.get_time()) and (not rospy.is_shutdown()):
                    #print(rospy.get_time())
                    self.velpub.publish(output)
                    r.sleep()

if __name__ == '__main__':
    turtle1 = Turtlebot()
    nav = Navigator()
    coordinates = nav.actualAStar((368,368),(500,200),"Maps/collected_maps_stage/library_lower.png")
    Converter = Path_To_Velocity(coordinates,1)
    commands = Converter.get_velocity_commands(15)
    turtle1.goForward(commands)
