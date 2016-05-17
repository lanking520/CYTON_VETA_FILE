#!/usr/bin/env python

import roslib
roslib.load_manifest('cyton_arm_controller')
import time
import rospy
from std_msgs.msg import Float64

joint_names = ( 'shoulder_roll_controller',
		'shoulder_pitch_controller',
		'elbow_roll_controller',
		'elbow_pitch_controller',
		'wrist_roll_controller',
		'wrist_pitch_controller',
		'wrist_yaw_controller',
		'gripper_open_controller',
)		

def move(a,b,c,d,e,f,g,h):
	joint_commands = (a,b,c,d,e,f,g,h)               
	pubs = [rospy.Publisher(name + '/command', Float64) for name in joint_names]
	rospy.init_node('cyton_veta', anonymous=True)
    
	for i in range(len(pubs)):
		pubs[i].publish(joint_commands[i])
	time.sleep(3)

if __name__ == '__main__':
#initial pos	
	print "Setting Home Position"
	move(0,0,0,0,0,0,0,0)

#shoulder roll
	print "Setting Shoulder Roll"
	move(4,0,0,0,0,0,0,0)
        move(-4,0,0,0,0,0,0,0)
        move(0,0,0,0,0,0,0,0)

#shoulder pitch
	print "Setting Shoulder Pitch"
        move(0,1.5,0,0,0,0,0,0)
        move(0,0,0,0,0,0,0,0)
	move(0,-1.5,0,0,0,0,0,0)
#elbow roll
	print "Setting Elbow Roll"
        move(0,0,0,0,0,0,0,0)
        move(0,0,4,0,0,0,0,0)
        move(0,0,-4,0,0,0,0,0)

#elbow pitch	
	print "Setting Elbow Pitch"
        move(0,0,0,0,0,0,0,0)
        move(0,0,0,1.5,0,0,0,0)
        move(0,0,0,0,0,0,0,0)
        move(0,0,0,-2,0,0,0,0)

#wrist roll
	print "Setting Wrist Roll"
        move(0,0,0,0,0,0,0,0)
        move(0,0,0,0,4,0,0,0)
        move(0,0,0,0,-4,0,0,0)
#wrist pitch
	print "Setting Wrist pitch"
        move(0,0,0,0,0,0,0,0)
        move(0,0,0,0,0,2,0,0)
        move(0,0,0,0,0,-2,0,0)
#wrist yaw
	print "Setting Wrist Yaw"
        move(0,0,0,0,0,0,0,0)
        move(0,0,0,0,0,0,2,0)
        move(0,0,0,0,0,0,0,0)
	move(0,0,0,0,0,0,-2,0)
#gripper
	print "Setting Gripper"
        move(0,0,0,0,0,0,0,2)
        move(0,0,0,0,0,0,0,0)
	move(0,0,0,0,0,0,0,-2)
        move(0,0,0,0,0,0,0,0)
