#!/usr/bin/env python

import sys
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

def help():
	print "Usage: python " + str(sys.argv[0]) + " [-4:4] [-1.5:1.5] [-4:4] [-2:1.5] [-4:4] [-2:2] [-2:2] [-2:2]"
	print "where the values are for:"
	print "     shoulder_roll shoulder_pitch elbow_roll elbow_pitch wrist_roll wrist_pitch wrist_yaw gripper_open"
	sys.exit(0)

def move(a,b,c,d,e,f,g,h):
	joint_commands = [ float(val) for val in [a,b,c,d,e,f,g,h]]               
	pubs = [rospy.Publisher(name + '/command', Float64) for name in joint_names]
	rospy.init_node('cyton_veta', anonymous=True)
    
	for i in range(len(pubs)):
		print("Trying to publish {} to servo {}".format(joint_commands[i], i))
		pubs[i].publish(joint_commands[i])
	time.sleep(3)

if __name__ == '__main__':
	if len(sys.argv) != 9:
		help()

	input1 = sys.argv[1]
	input2 = sys.argv[2]
	input3 = sys.argv[3]
	input4 = sys.argv[4]
	input5 = sys.argv[5]
	input6 = sys.argv[6]
	input7 = sys.argv[7]
	input8 = sys.argv[8]

	if input1 < -4 and input1 > 4:
		help()
	if input2 < -1.5 and input2 > 1.5:
		help()
	if input3 < -4 and input3 > 4:
		help()
	if input4 < -2 and input4 > 1.5:
		help()
	if input5 < -4 and input5 > 4:
		help()
	if input6 < -2 and input6 > 2:
		help()
	if input7 < -2 and input7 > 2:
		help()
	if input8 < -2 and input8 > 2:
		help()

	#initial pos
	print "Setting Home Position"
	move(0, 0, 0, 0, 0, 0, 0, 0)

	print "Position selected"
	move(input1, input2, input3, input4, input5, input6, input7, input8)
