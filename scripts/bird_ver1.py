#!/usr/bin/env python3

import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# Define the mouse callback function
'''def get_pixel(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONUP:
        print("Pixel location: ({}, {})".format(x, y))'''

def points (image : Image):
    
    bridge = CvBridge()
    img= bridge.imgmsg_to_cv2(image, 'bgr8')
    #img = np.frombuffer(image.data, dtype=np.uint8).reshape(image.height, image.width, -1)
    #cv2.imshow('image', img)
    
    #print(image.width, image.height)

    #src =  np.float32([(0,image.height/2.7), (image.width, image.height/2.7), (0, image.height),(image.width, image.height)])
    src =  np.float32([(73,113), (255, 113), (1, 147),(319, 143)])
    #src =  np.float32([(105,131), (208, 132), (0, image.height),(image.width, image.height)])
    dst = np.float32([(0,0), (image.width, 0), (0, image.height),(image.width, image.height) ])

    M = cv2.getPerspectiveTransform(src, dst)

    birdseye_img = cv2.warpPerspective(img, M, (image.width, image.height))
    #cv2.imshow('Birdseye View', birdseye_img)
    #cv2.setMouseCallback('image', get_pixel)

    image = bridge.cv2_to_imgmsg(birdseye_img, encoding='bgr8')
    pub.publish(image)

    #cv2.waitKey(1)


if __name__ == '__main__' :
    
    rospy.init_node("BIRD_VIEW")
    #pub1=rospy.Publisher("/camera/color/pixels", Image, queue_size=10)
    pub=rospy.Publisher("/camera/color/bird_view", Image, queue_size=10)
    sub = rospy.Subscriber("/camera/color/image_raw", Image, callback = points)
    
    rospy.spin()
