'''
Gamepad Program with Client station embedded
Author: Qing Lan
Copyright: Free
Date: 1/2/2016
'''
import socket
import time
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import roslib  #Basic library for ROS
roslib.load_manifest('cyton_arm_controller')
from std_msgs.msg import Float64
import rospy #ROS library for python

s = socket.socket()         # Create a socket object
host = '192.168.40.20'     # Get local machine IP
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.
c, addr = s.accept()     # Establish connection with client.

################################ Variable Class
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
	    self.select = not self.select

    def get_position(self):
	 return self.move_position

    def get_start(self):
	 return self.start

    def get_select(self):
         return self.select

################################# Arm Class
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
################################# Class Packet: Major class of reading packet
class packet:
	def __init__(self):
		self.packet_recv = []
		self.packet_lost = []
		self.packet_counter = 0
		self.packet_label = 0
		self.timer = 0
		self.time_delay = 0
		self.dead_packet = 0
		self.out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.out_last = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 

	def packet_record(self):
		self.packet_recv.append(self.packet_counter)
		self.packet_lost.append(self.dead_packet)
		self.packet_counter = 0
		self.dead_packet = 0
	
	def timer_probe(self, time_set):
		self.timer +=1 * time_set

	def get_timer(self):
		return self.timer

	def drawer(self, canvas):
		canvas.draw_text('Packet Number: ' + str(self.packet_label), (10, 460), 20, 'White')
		canvas.draw_text('Packet Loss: ' + str(self.dead_packet), (10, 480), 20, 'White')
		canvas.draw_text('Total packet Reveived: ' + str(self.packet_counter), (10, 520), 20, 'White')
		canvas.draw_text('Packet Time Delay: '+ str(self.time_delay), (10, 500), 20, 'White')

	def joystick(self):
    		try:
        		self.out = list(eval(c.recv(1024))) # stop here waiting for packet
        		self.out_last = self.out
			self.packet_counter += 1
			self.time_delay = self.timer
			self.timer = 0
			self.packet_label = self.out[16]
			self.dead_packet = self.packet_label - self.packet_counter
        		c.settimeout(5.0)
    		except:
			self.out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,self.out_last[-1]]
    			#s.close                     # Close the socket when done
    		return self.out
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
def packet_updater():
	packet_ana.timer_probe(0.1)
	if packet_ana.get_timer() == 2:
		packet_ana.packet_record()
	


def main():
    global out
    variable.translation(packet_ana.joystick())
    if variable.get_start():
       cyton.update(variable.get_position())
       cyton.move()
    else:
       cyton.home()

def draw(canvas):
    position = cyton.get_position()
    name = cyton.get_joint_names()
    select_result = variable.get_select()
    packet_ana.drawer(canvas)
    canvas.draw_line((600, 0), (600, 600), 4, 'White')
    canvas.draw_text('Current Mode', (10, 400), 30, 'White')
    #canvas.draw_text('Package Received :' + str(package), (10, 440), 20, 'White') 
    for i in range (len(name)):
    	canvas.draw_text(name[i] + ' Status: ' + str(position[i]), (10, 20 + 25*i), 20, 'White')

packet_ana = packet()
variable = global_variable(600, 800)
cyton = arm(0.02)
robot = simplegui.create_frame("Cyton Controller Joystick",variable.width, variable.height, 0)
cyton.home() # Should be placed before any 'Start' or there will be error
robot.set_draw_handler(draw)
draw_timer = simplegui.create_timer(30, main)
packet_update = simplegui.create_timer(100, packet_updater)
#joy_stick_timer= simplegui.create_timer(50, joystick)
draw_timer.start()
packet_update.start()
#joy_stick_timer.start()
robot.start()
cyton.home()

