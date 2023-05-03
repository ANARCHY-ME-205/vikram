#!/usr/bin/env python3

import rospy
import sys
import select
import tty
import termios
from geometry_msgs.msg import Twist

# Initialize the node
rospy.init_node('turtle_teleop_key')

# Initialize the twist message
twist = Twist()

# Set the linear and angular velocities to zero
twist.linear.x = 0.0
twist.angular.z = 0.0

# Set the maximum linear and angular velocities
max_linear_vel = 0.5  # meters per second
max_angular_vel = 0.5  # radians per second

# Initialize the publisher to the /cmd_vel topic
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

# Define a function to get a single character from the keyboard
def get_key():
    # Save the terminal attributes
    old_attr = termios.tcgetattr(sys.stdin)
    
    try:
        # Set the terminal to raw mode
        tty.setraw(sys.stdin.fileno())
        
        # Check if a key has been pressed
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            # Read the key from the keyboard
            key = sys.stdin.read(1)
        else:
            key = None
    finally:
        # Restore the terminal attributes
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
    
    return key

# Define the control keys
forward_key = 'w'
backward_key = 's'
left_key = 'a'
right_key = 'd'
stop_key = ' '



# Loop to receive and process key inputs
while not rospy.is_shutdown():
    # Get the pressed key
    key = get_key()
    
    
    # Set the linear and angular velocities based on the pressed key
    if key == forward_key :
        twist.linear.x = max_linear_vel
        twist.angular.z = 0.0
    elif key == backward_key :
        twist.linear.x = -max_linear_vel
        twist.angular.z = 0.0
    elif key == left_key :
        twist.angular.z = max_angular_vel
    elif key == right_key :
        twist.angular.z = -max_angular_vel
    elif key == stop_key:
        twist.linear.x = 0.0
        twist.angular.z = 0.0

    # Publish the twist message
    pub.publish(twist)
