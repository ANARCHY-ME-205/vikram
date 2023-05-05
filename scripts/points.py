#!/usr/bin/env python3

import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge 

def points(image : Image) : 

    bridge = CvBridge()
    # Load the depth image
    depth_image = bridge.imgmsg_to_cv2(image,'32FC1')
    cv2.imshow("ORIGINAL IMAGE",depth_image)
    # Define camera parameters
    fx = 277.19135641132203
    fy = 277.19135641132203
    cx = 160.5
    cy = 120.5

    # Create a matrix of the intrinsic parameters
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

    # Define camera extrinsic parameters (for example, assume the camera is at the origin and pointing along the z-axis)
    R = np.eye(3)  # rotation matrix
    t = np.zeros((3, 1))  # translation vector

    # Convert the depth image to a point cloud
    rows, cols = depth_image.shape[:2]
    points = np.zeros((rows, cols, 3))
    for u in range(cols):
        for v in range(rows):
            depth = depth_image[v, u] / 1000.0  # convert from millimeters to meters
            if depth == 0:
                continue
            else:
                x = (u - cx) * depth / fx
                y = (v - cy) * depth / fy
                z = depth
                points[v, u] = [x, y, z]

    # Visualize the point cloud
    cv2.imshow('Point cloud', points)
    cv2.waitKey(1)
  
if __name__ == '__main__':
    rospy.init_node('point')
    #pub=rospy.Publisher("/camera/color/bird_view", Image, queue_size=10)
    sub = rospy.Subscriber("/camera/depth/image_raw",Image, callback=points)
    rospy.spin()