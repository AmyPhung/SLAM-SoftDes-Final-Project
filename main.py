import rospy
from convert_path_to_velocity import Path_To_Velocity
from geometry_msgs.msg import Vector3, Twist, PoseStamped, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from Navigator import Navigator
from PublishingVelocities import Turtlebot
class MainClass:
    def __init__(self):
        rospy.init_node("mainNode")
        rospy.Subscriber("/amcl_pose",PoseWithCovarianceStamped,self.storeOdometry)
        rospy.Subscriber("/move_base_simple/goal",PoseStamped,self.goToThisPoint)
        self.conversionFactor = 0.05

    def storeOdometry(self,msg):
        self.pose = msg.pose.pose.position
    def goToThisPoint(self,msg):
        placeToGoTo = msg.pose.position
        positionInMapDest = self.positionToPixels(placeToGoTo)
        positionInMapStart = self.positionToPixels(self.pose)
        print(positionInMapStart,positionInMapDest)
        nav = Navigator()
        coordinates = nav.actualAStar(positionInMapStart,positionInMapDest,"Maps/collected_maps_stage/cc3.png") # get the path
        Converter = Path_To_Velocity(coordinates,1)
        commands = Converter.get_velocity_commands(10) # convert the path to velocities
        turtle1 = Turtlebot()
        turtle1.publishVelocities(commands)
    def positionToPixels(self,pose):
        return (int((pose.x - 8.0) / self.conversionFactor + 500),int(-1*(pose.y + 5.5) / self.conversionFactor + 1050))
if __name__ == '__main__':
    main = MainClass()
    rospy.spin()
