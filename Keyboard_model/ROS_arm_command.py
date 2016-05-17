#!/usr/bin/env python
"""
The module include ROS and SimpleGUI. SimpleGUI originally created by Rice University, which contains the java definition on of the python library. To properly use it in python, a module called SimpleGUICS2Pygame are applied to add in the python library. Please check 
http://www.codeskulptor.org to see more info of simpleGUI and 
https://simpleguics2pygame.readthedocs.org/ for simpleguics2pygame
"""
import roslib  #Basic library for ROS
roslib.load_manifest('cyton_arm_controller')
import time
import rospy #ROS library for python
import serial #Pyserial module
from std_msgs.msg import Float64
try:
    import simplegui #SimpleGUI GUI module
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

#.........Global variable............................
#Simple GUI Module
WIDTH = 400
HEIGHT = 400
#Live variable
joint_current = [0,0,0,0,0,0,0,0]
controller = 0
move_val = [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
Move = False
click = False
velocity = 0
#Constant value
joint_angle_limit = ([-150,150], [-90, 90],[-150,150],[-120,120], [-150,150],[-100,100],[-200,200],[0,180])
joint_val_limit = ([-4,4], [-1.5,1.5], [-4,4], [-2,1.5], [-4,4], [-2,2], [-2,2], [-2,2])
joint_names = ( 'shoulder_roll_controller',
        'shoulder_pitch_controller',
        'elbow_roll_controller',
        'elbow_pitch_controller',
        'wrist_roll_controller',
        'wrist_pitch_controller',
        'wrist_yaw_controller',
        'gripper_open_controller',
)

#.....................End of Def Variable...............
#...................CYTON Handler......................
def move():
    global joint_current,Move,click
    for i in range(len(joint_current)):
	joint_current[i]= round(joint_current[i],3)
    if Move:
	if click:
		joint_commands = tuple(joint_current)          
		pubs = [rospy.Publisher(name + '/command', Float64) for name in joint_names]
		rospy.init_node('cyton_veta', anonymous=True)
    
		for i in range(len(pubs)):
			pubs[i].publish(joint_commands[i])
		print joint_current
		pass
def force_sensor():
	pass
#...................Draw Handler.......................
def val_angle(angle_set,val_set,val):
    return (angle_set[1] - angle_set[0]) * val / (val_set[1] - val_set[0])  

def draw(canvas):
    global joint_angle_limit, joint_names, joint_val_limit, controller, joint_current
    if Move:
        #if joint_current[controller] >= joint_val_limit[controller][0] and 			joint_current[controller] <= joint_val_limit[controller][1]:
        joint_current[controller] += velocity
        Output = 'Active'
        color = 'Green'
        data = ""
        data =joint_names[controller] + ' Angle: ' +str(val_angle(joint_angle_limit[controller],joint_val_limit[controller], joint_current[controller])) +' Degree'
        canvas.draw_text(data, (10, 20), 20, 'White')
    else:
        canvas.draw_text('Please wait arm moving to home', (10, 20), 20, 'White')
        Output = 'Disabled'
        color = 'Red'
    canvas.draw_text('Controller Status:'+ Output, (20, 390), 20, color)
    canvas.draw_text('Current joint Value:', (20, 320), 20, 'White')
    canvas.draw_text(str(joint_current), (20, 350), 20, 'White')
	
#...................Button handler...................
def start():
    global Move
    Move = True

def shoulder_roll():
    global controller
    controller = 0

def shoulder_pitch():
    global controller
    controller = 1

def elbow_roll():
    global controller
    controller = 2

def elbow_pitch():
    global controller
    controller = 3

def wrist_roll():
    global controller
    controller = 4

def wrist_pitch():
    global controller
    controller = 5
    
def wrist_yaw():
    global controller
    controller = 6

def grip_open():
    global controller
    controller = 7

def go_home():
    global joint_current, Move, click
    joint_current = [0,0,0,0,0,0,0,0]
    click = True
    move()
    Move = False
    click = False
#...................key handler.....................
def keydown(key):
    global controller,move_val,velocity, click
    if Move:
	click = True
        if key == simplegui.KEY_MAP["up"]:
            velocity = move_val[controller]
        elif key == simplegui.KEY_MAP["down"]:
            velocity = -move_val[controller]

def keyup(key):
    global velocity, click
    click = False
    if key == simplegui.KEY_MAP["up"]:
        velocity = 0
    elif key == simplegui.KEY_MAP["down"]:
        velocity = 0
#...................End of Def......................
robot = simplegui.create_frame("CYTON control Interface", WIDTH, HEIGHT)
robot.add_button("Start",start)
robot.add_button("shoulder_roll_controller",shoulder_roll)
robot.add_button("shoulder_pitch_controller",shoulder_pitch)
robot.add_button("elbow_roll_controller",elbow_roll)
robot.add_button("elbow_pitch_controller",elbow_pitch)
robot.add_button("wrist_roll_controller",wrist_roll)
robot.add_button("wrist_pitch_controller",wrist_pitch)
robot.add_button("wrist_yaw_controller",wrist_yaw)
robot.add_button("gripper_open_controller",grip_open)
robot.add_button("Home position",go_home)
robot.set_keydown_handler(keydown)
robot.set_keyup_handler(keyup)
robot.set_draw_handler(draw)
move_timer = simplegui.create_timer(100, move)
force_timer = simplegui.create_timer(100, force_sensor)
move_timer.start()
force_timer = start()

robot.start()
go_home()
