#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import cv_bridge
import time

image_index = 0
time_stamp = 0
def callback(data):
    global image_index 
    global time_stamp
    bridge = cv_bridge.CvBridge()
    rospy.loginfo("received an image")
    img = bridge.imgmsg_to_cv2(data)
    #cv2.imshow('image', img)
    curr_time = time.time()
    if(curr_time - time_stamp >= 1):
        cv2.imwrite('data/{}.png'.format(image_index), img)
        image_index += 1
        time_stamp = curr_time
    
def listener():

    rospy.init_node('image_grabber', anonymous=True)

    rospy.Subscriber("/camera/rgb/image_raw", Image, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

