#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import cv_bridge

image_index = 0

def callback(data):
    global image_index 
    bridge = cv_bridge.CvBridge()
    rospy.loginfo("received an image")
    img = bridge.imgmsg_to_cv2(data)
    #cv2.imshow('image', img)
    cv2.imwrite('data/{}.png'.format(image_index), img)
    image_index += 1
    
def listener():

    rospy.init_node('image_grabber', anonymous=True)

    rospy.Subscriber("/camera/rgb/image_raw", Image, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

