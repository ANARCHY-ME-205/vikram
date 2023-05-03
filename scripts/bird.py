#!/usr/bin/env python3



import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge 

def conversion(image : Image ):

    bridge = CvBridge()
    img= bridge.imgmsg_to_cv2(image, 'bgr8')
    #cv2.imshow("ORIGINAL IMAGE", img)
    focal_length_x = 277.19135641132203
    focal_length_y = 277.19135641132203
    principal_point_x = 160.5
    principal_point_y = 120.5
    # Define the intrinsic matrix of the camera
    #K: [277.19135641132203, 0.0, 160.5, 0.0, 277.19135641132203, 120.5, 0.0, 0.0, 1.0]
    K = np.array([[focal_length_x, 0, principal_point_x],
                [0, focal_length_y, principal_point_y],
                [0, 0, 1]])
    #100,140; 218,140
    # Define the corresponding points in the image and the bird's eye view
    x1=100
    y1=140
    x2=218
    y2=140
    x3=0
    y3=240
    x4=320
    y4=240

    image_points = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    birdseye_points = np.array([[0, 0], [image.width, 0], [0, image.height], [image.width, image.height]])

    # Compute the homography matrix using the corresponding points
    H, _ = cv2.findHomography(image_points, birdseye_points)

    # Define the homography matrix for the bird's eye view
    '''H = np.array([[homography_00, homography_01, homography_02],
                [homography_10, homography_11, homography_12],
                [homography_20, homography_21, homography_22]])'''

    # Capture an image using the camera
    #img = cv2.imread('image.jpg')

    # Undistort the image using the intrinsic matrix
    undistorted_img = cv2.undistort(img, K, None, newCameraMatrix=K)
    
    # Compute the bird's eye view of the image using the homography matrix
    birdseye_img = cv2.warpPerspective(undistorted_img, H, (image.width, image.height))
    image = bridge.cv2_to_imgmsg(birdseye_img, encoding='bgr8')
    # Display the bird's eye view of the image
    #cv2.imshow('Birdseye View', birdseye_img)
    pub.publish(image)
    #cv2.waitKey(1)
    

if __name__ == '__main__':
    rospy.init_node("BIRD_VIEW")
    pub=rospy.Publisher("/camera/color/bird_view", Image, queue_size=10)
    sub = rospy.Subscriber("/camera/color/image_raw",Image, callback=conversion)
    rospy.spin()
