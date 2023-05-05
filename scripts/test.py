#!/usr/bin/env python3

import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge 
import math

'''K: [277.19135641132203, 0.0, 160.5, 0.0, 277.19135641132203, 120.5, 0.0, 0.0, 1.0]
R: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
P: [277.19135641132203, 0.0, 160.5, -0.0, 0.0, 277.19135641132203, 120.5, 0.0, 0.0, 0.0, 1.0, 0.0]
camera : <pose>0.6587 -0 1.17747 0.006839 0.098516 0.000914</pose>
'''

def conversion(image : Image ):

    bridge = CvBridge()
    img= bridge.imgmsg_to_cv2(image, 'bgr8')
    cv2.imshow("ORIGINAL IMAGE", img)
    K = np.array([[277.19135641132203, 0.0, 160.5],
                [0.0, 277.19135641132203, 120.5],
                [0.0, 0.0, 1.0]])
    R = np.array([[1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]])
    P = np.array([[277.19135641132203, 0.0, 160.5, 0.0],
                [0.0, 277.19135641132203, 120.5, 0.0],
                [0.0, 0.0, 1.0, 0.0]])

    rt = np.array([[1.0, 0.0, 0.0, 0.6587],
                  [0.0, 1.0, 0.0, 0],
                  [0.0, 0.0, 1.0, 1.17747]])
    
    




    

if __name__ == '__main__':
    rospy.init_node("BIRD_VIEW")
    #pub=rospy.Publisher("/camera/color/bird_view", Image, queue_size=10)
    sub = rospy.Subscriber("/camera/color/image_raw",Image, callback=conversion)
    rospy.spin()
