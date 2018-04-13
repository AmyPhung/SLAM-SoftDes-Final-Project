# rostopic pub -r 10 /cmd_vel geometry_msgs/Twist  '{linear:  {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'

#!/usr/bin/env python
# license removed for brevity
import rospy
from nav2d_operator.msg import cmd

def publish_velocity():
    rospy.init_node('vel_test')
    velocity_publisher = rospy.Publisher('cmd', cmd, queue_size=10)
    vel_msg = cmd()

    vel_msg.Velocity = -1
    vel_msg.Turn = 10

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_velocity()
    except rospy.ROSInterruptException:
        pass
