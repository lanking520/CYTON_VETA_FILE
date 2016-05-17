'''
Program to save and store the formula from pressure sensor
Author: Qing Lan
Copyright: Free
Date: 1/2/2016
'''
import pygame	#function to configure the gamepad
import serial	#get the board data from serial port
import os 	#use to store as a file
import time
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import roslib  #Basic library for ROS
roslib.load_manifest('cyton_arm_controller')
from std_msgs.msg import Float64
import rospy #ROS library for python

#initialize the environment
pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()
board = serial.Serial('/dev/ttyACM0',9600, timeout = 5)

class global_variable:
    def __init__(self, height, width):
        #Basic information
        self.height = height
        self.width = width
        #determine the start of movement
        self.start = True
	self.select = False
        #Position needed to send to the controller
        self.move_position = [0,0,0,0,0,0,0,0]

    def translation(self, command):
	#Analog Controller
	self.move_position[0]= -command[0]
	self.move_position[1]= command[1]
	self.move_position[2]= -command[2]
	self.move_position[3]= -command[3]
	#button Controller
	self.move_position[4]= command[4]-command[6]
	self.move_position[5]= command[5]-command[7]
	self.move_position[6]= command[8]-command[9]
	self.move_position[7]= command[10]-command[11]
	#Red_button Start
	if (command[13]==1):
	    self.start = False
	else:
	    self.start = True
	if (command[12]==1):
	    self.select = True
	else:
            self.select = False

    def get_position(self):
	 return self.move_position

    def get_start(self):
	 return self.start

    def get_select(self):
         return self.select

class arm:
    def __init__(self, move):
        #Position and Joint movement limits
        self.position = [0,0,0,0,0,0,0,0]
        self.move_scale = move
        self.joint_val_limit = ([-2.7,2.7], [-1.5,1.5], [-2.6,2.6], [-2,1.5], [-2.6,2.6], [-2,1.8], [-1.7,1.8], [-1,1])
        self.joint_names = ( 'shoulder_roll_controller',
        'shoulder_pitch_controller',
        'elbow_roll_controller',
        'elbow_pitch_controller',
        'wrist_roll_controller',
        'wrist_pitch_controller',
        'wrist_yaw_controller',
        'gripper_open_controller',
)
    def move(self):
        #core function in moving arm
        joint_commands = tuple(self.position)          
        pubs = [rospy.Publisher(name + '/command', Float64) for name in self.joint_names]
	rospy.init_node('cyton_veta', anonymous=True)
        for i in range(len(pubs)):
            pubs[i].publish(joint_commands[i])
            
    def update(self, current_position = [0,0,0,0,0,0,0,0]):
        for i in range(len(current_position)):
            self.position[i] += current_position[i]*self.move_scale
            #Check the value in operating range
            if (self.position[i]>=self.joint_val_limit[i][1]):
            	self.position[i]=self.joint_val_limit[i][1]
            if (self.position[i]<=self.joint_val_limit[i][0]):
            	self.position[i]=self.joint_val_limit[i][0]
      
    def home(self):
	self.position= [0,0,0,0,0,0,0,0]	
	self.move()

    def get_position(self):
	return self.position
    
    def get_joint_names(self):
	return self.joint_names

class pressure_storage:
    def __init__(self):
	self.pressure_val = 0
	self.file_list = [[0,0]]

    def get_pressure_val(self):
	return self.pressure_val

    def get_list(self):
	return self.file_list

    def pass_pressure(self):
	temp = board.readline()
	try:
		self.pressure_val = float(temp)
		print self.pressure_val
	except Exception,e:
		print str(e)
	board.flush()
	board.flushInput()

    def store_val(self, gripper_val):
	if (self.pressure_val != self.file_list[-1][1]):
		self.file_list.append([gripper_val,self.pressure_val])	
    
    def store_to_file(self, file_name):
	my_file = open(file_name, 'w')
	for i in range(len(self.file_list)):
		my_file.write(str(self.file_list[i][0]) + ',' + str(self.file_list[i][1])+'\n')
	my_file.close()

"""
REMEMBER: The gamepad controller should be operated into ANALOG
The output format (out[16]:
Left Stick: Left -1 Right 1
Left Stick: Up -1 Down 1
Right Stick: Left -1 Right 1
Right Stick: Up -1 Down 1
1 2 3 4 buttons
L1 R1 L2 R2 buttons
SELECT START Left_Stick_push Right_Stick_push
"""
def joystick():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0 #iterator
    pygame.event.pump()
    
    #Read input from the two joysticks       
    for i in range(0, joy.get_numaxes()):
        out[it] = joy.get_axis(i)
        it+=1
    #Read input from buttons
    for i in range(0, joy.get_numbuttons()):
        out[it] = joy.get_button(i)
        it+=1
    return out

def main():
    variable.translation(joystick())
    select_result = variable.get_select()
    position = cyton.get_position()
    if select_result:
	myfile.store_val(position[7])
    if variable.get_start():
       cyton.update(variable.get_position())
       cyton.move()
    else:
       cyton.home()

def draw(canvas):
    width = 510 #width for the stored point
    weight = 0 #Adding more rows
    position = cyton.get_position()
    name = cyton.get_joint_names()
    point_list = myfile.get_list()
    pressure = myfile.get_pressure_val()
    canvas.draw_line((500, 0), (500, 600), 4, 'White')
    canvas.draw_text('Pressure Val ' + str(pressure), (10, 400), 30, 'White')
    canvas.draw_text('Stored Point', (510, 20), 30, 'White')
    for i in range (len(name)):
    	canvas.draw_text(name[i] + ' Status: ' + str(position[i]), (10, 20 + 25*i), 20, 'White')
    
    for i in range (len(point_list)):
	height = 40 + 18*i - (variable.height) * weight
	if height > variable.height:
		width +=100
		weight +=1
	canvas.draw_text(str(point_list[i]), (width, height), 15, 'White')


variable = global_variable(600, 800)
cyton = arm(0.02)
myfile = pressure_storage();
robot = simplegui.create_frame("Cyton Controller Joystick",variable.width, variable.height, 80)

cyton.home() # Should be placed before any 'Start' or there will be error
robot.add_input('File name', myfile.store_to_file, 50)
robot.set_draw_handler(draw)
draw_timer = simplegui.create_timer(30, main)
pressure_timer = simplegui.create_timer(50, myfile.pass_pressure)
draw_timer.start()
pressure_timer.start()
robot.start()
cyton.home()
