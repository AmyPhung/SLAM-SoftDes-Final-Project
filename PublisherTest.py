# rostopic pub -r 10 /cmd_vel geometry_msgs/Twist  '{linear:  {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'
"""
Test code for publishing commands to simulated robot
"""
#!/usr/bin/env python
# license removed for brevity
import rospy
from nav2d_operator.msg import cmd
from geometry_msgs.msg import Twist

def publish_velocity():
    """
    Publishes velocity and heading commands to rostopic /cmd
    """
    rospy.init_node('vel_test')
    velocity_publisher = rospy.Publisher('cmd', cmd, queue_size=10)
    vel_msg = cmd()

    vel_msg.Velocity = -10
    vel_msg.Turn = .1 #how much to turn (changes turn radius)
    vel_msg.Mode = 1


    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rate.sleep()
def convert_velocity():
    rospy.init_node('listener')

    rospy.Subscriber('cmd_vel', Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        publish_velocity()
        convert_velocity()
    except rospy.ROSInterruptException:
        pass
