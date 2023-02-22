#! /usr/bin/env python3
"""
This Node takes the data from the /odom topic and publishes the odom to base_link frame
"""

import rospy
import tf
import sys
import numpy as np
from nav_msgs.msg import Odometry
from time import sleep

prev_transform = np.array((-1,-1,-1))
prev_rotation = np.array((0,0,0,0))

def odom_callback(msg):
    global pub
    # print(msg)
    global prev_transform
    global sim
    global prev_rotation
    transform = np.array((msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z))
    rotation = np.array((msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w))
    if np.linalg.norm(transform-prev_transform) < 0.04 and np.linalg.norm(rotation-prev_rotation) < 0.04:
        return
    # print(msg)
    prev_transform = transform
    prev_rotation = rotation
    br = tf.TransformBroadcaster()
    print('publishing transform')
    br.sendTransform((msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z),
                     (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w),
                     rospy.Time.now(),
                     "base_link",
                     "odom")
    if not sim:
        # print('sending')
        pub.publish(msg)



if __name__ == '__main__':
    rospy.init_node('odom_to_base_link_transform')
    print('################')
    sim = rospy.get_param("mode") == 'sim'
    print(sim)
    # TODO change topic based on value of sim
    topic = '/odom' if sim else '/zed2i/zed_node/odom'
    rospy.Subscriber(topic, Odometry, odom_callback)
    pub = rospy.Publisher('/odom', Odometry, queue_size=10)
    rospy.spin()
