'''
Program to save and store the formula from pressure sensor
Author: Qing Lan
Copyright: Free
Date: 1/2/2016
'''
import pygame  # function to configure the gamepad
import math
import serial  # get the board data from serial port
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import roslib  # Basic library for ROS
roslib.load_manifest('cyton_arm_controller')
from std_msgs.msg import Float64
import rospy  # ROS library for python

# initialize the environment
pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()


########################################## Central Variable Class
class global_variable:
    def __init__(self, height, width):
        # Basic information
        self.height = height
        self.width = width
        # determine the start of movement
        self.start = True
        self.select = False
        # Position needed to send to the controller
        self.move_position = [0, 0, 0, 0, 0, 0, 0, 0]

    def translation(self, command):
        # Analog Controller
        self.move_position[0] = -command[0]
        self.move_position[1] = command[1]
        self.move_position[2] = -command[2]
        self.move_position[3] = -command[3]
        # button Controller
        self.move_position[4] = command[4] - command[6]
        self.move_position[5] = command[5] - command[7]
        self.move_position[6] = command[8] - command[9]
        # self.move_position[7]= command[10]-command[11] #Disabled in this function
        # Red_button Start
        if (command[13] == 1):
            self.start = False
        else:
            self.start = True
        if (command[12] == 1):
            self.select = True
        else:
            self.select = False

    def get_position(self): # Return the velocity information
        return self.move_position

    def get_start(self):
        return self.start

    def get_select(self):
        return self.select

    def set_gripper(self, value):  # Terminal to receive the gripper velocity
        variable.move_position[7] = value


######################################### ROS Class
class arm:
    def __init__(self, move):
        # Position and Joint movement limits
        self.position = [0, 0, 0, 0, 0, 0, 0, 0]
        self.move_scale = move
        self.joint_val_limit = (
        [-2.7, 2.7], [-1.5, 1.5], [-2.6, 2.6], [-2, 1.5], [-2.6, 2.6], [-2, 1.8], [-1.7, 1.8], [-1, 1])
        self.joint_names = ('shoulder_roll_controller',
                            'shoulder_pitch_controller',
                            'elbow_roll_controller',
                            'elbow_pitch_controller',
                            'wrist_roll_controller',
                            'wrist_pitch_controller',
                            'wrist_yaw_controller',
                            'gripper_open_controller',
                            )

    def move(self):
        # core function in moving arm
        joint_commands = tuple(self.position)
        pubs = [rospy.Publisher(name + '/command', Float64) for name in self.joint_names]
        rospy.init_node('cyton_veta', anonymous=True)
        for i in range(len(pubs)):
            pubs[i].publish(joint_commands[i])

    def update(self, current_position=[0, 0, 0, 0, 0, 0, 0, 0]):
        for i in range(len(current_position)):
            self.position[i] += current_position[i] * self.move_scale
            # Check the value in operating range
            if (self.position[i] >= self.joint_val_limit[i][1]):
                self.position[i] = self.joint_val_limit[i][1]
            if (self.position[i] <= self.joint_val_limit[i][0]):
                self.position[i] = self.joint_val_limit[i][0]

    def home(self):
        self.position = [0, 0, 0, 0, 0, 0, 0, -1]
        self.move()

    def get_position(self):
        return self.position

    def get_gripper(self):  # Port to get the gripper current value
        return self.position[7]

    def get_joint_names(self):
        return self.joint_names


################################## Pressure sensor and Communication Class
class pressure_storage:
    def __init__(self, location):
        self.pressure_val = 0.15
        self.file_list = [[0, 0]]
        self.board = serial.Serial(location, 115200, timeout=5)
        self.movement = 60.0
	self.prev = 0.15

    def get_pressure_val(self):
        return self.pressure_val

    def get_list(self):
        return self.file_list

    def pass_pressure(self):
        temp = self.board.readline()
        try:
            pressure_val = float(temp)
            if abs(self.prev - pressure_val) >= 2:
		self.pressure_val = self.prev
	    else:
		self.prev = pressure_val 
		self.pressure_val = pressure_val
            # print self.pressure_val
        except Exception, e:
            print str(e)
        self.board.flush()
        self.board.flushInput()

    def write_val(self, matched, value):
        if matched:
            # move_prev = self.movement
            self.movement = value
                # if move_prev - self.movement != 0:
            self.board.write(str(self.movement) + '\n')

    def store_val(self, gripper_val):
        if (self.pressure_val != self.file_list[-1][1]):
            self.file_list.append([gripper_val, self.pressure_val])

    def store_to_file(self, file_name):
        my_file = open(file_name, 'w')
        for i in range(len(self.file_list)):
            my_file.write(str(self.file_list[i][0]) + ',' + str(self.file_list[i][1]) + '\n')
        my_file.close()

    def get_movement(self):
        return self.movement


##################################### Matching data class
class matching:
    def __init__(self):
        self.target_pressure = 0.15
        self.current_pressure = 0.15
        self.matched = True

    def set_target_pressure(self, target):
	if target <= 10 and target > 0.15:
        	self.target_pressure = target
    def set_current_pressure(self, current):
        self.current_pressure = current

    def matching_val(self):
        value = self.target_pressure - self.current_pressure
        if math.fabs(value) <= 0.05:  # Error rate
            self.matched = True
        else:
            self.matched = False
        if not self.matched:
            return value 
        else:
            return 0.0

    def get_match(self):
        return self.matched

    def get_target(self):
	return self.target_pressure


###############################################Gripper Class
class gripper:
    def __init__(self, buttom=[0, 0], limit=[-1, 1]):
        self.b = buttom
        self.border_limit = limit
        self.current_val = 0
        self.pressure_val = 0

    def mapping(self, input_val, pressure):
        self.current_val = (-self.border_limit[0] + input_val) / (-self.border_limit[0] + self.border_limit[1])
        self.pressure_val = pressure

    def get_current(self):
        return self.current_val

    def drawer(self, canvas):
        canvas.draw_polyline([[self.b[0] - 70, self.b[1]], [self.b[0] + 70, self.b[1]]], 10, 'Gray')
        canvas.draw_circle([self.b[0], self.b[1] + 20], 20, 3, 'White', 'Gray')
        scale = self.current_val * 40
        canvas.draw_polygon([[self.b[0] - 40 + scale, self.b[1] - 5], [self.b[0] - 70 + scale, self.b[1] - 5],
                             [self.b[0] - 40 + scale, self.b[1] - 50]], 3, 'Silver')
        canvas.draw_polygon([[self.b[0] + 40 - scale, self.b[1] - 5], [self.b[0] + 70 - scale, self.b[1] - 5],
                             [self.b[0] + 40 - scale, self.b[1] - 50]], 3, 'Silver')
        canvas.draw_circle([self.b[0] + 20 * math.sin(self.current_val * 2 * math.pi),
                            self.b[1] + 20 + 20 * math.cos(self.current_val * 2 * math.pi)], 2, 3, 'Blue')
        canvas.draw_circle([self.b[0] - 20 * math.sin(self.current_val * 2 * math.pi),
                            self.b[1] + 20 - 20 * math.cos(self.current_val * 2 * math.pi)], 2, 3, 'Green')
        canvas.draw_text('Current position: ' + str(self.current_val), [self.b[0] + 100, self.b[1]], 18, 'White')


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
    out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    it = 0  # iterator
    pygame.event.pump()

    # Read input from the two joysticks
    for i in range(0, joy.get_numaxes()):
        out[it] = joy.get_axis(i)
        it += 1
    # Read input from buttons
    for i in range(0, joy.get_numbuttons()):
        out[it] = joy.get_button(i)
        it += 1
    return out


def pass_pressure():
    myfile.pass_pressure()
    haptic.pass_pressure()
    cyton_gripper.mapping(cyton.get_gripper(), myfile.get_pressure_val())
    matched = match.get_match()
    if matched:
        match.set_target_pressure(haptic.get_pressure_val())
    match.set_current_pressure(myfile.get_pressure_val())
    movement = 80 - 50 * cyton_gripper.get_current()
    haptic.write_val(matched, movement)
    haptic_gripper.mapping(haptic.get_movement(), haptic.get_pressure_val())


def main():
    variable.translation(joystick())
    variable.set_gripper(match.matching_val())
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
    width = 510  # width for the stored point
    weight = 0  # Adding more rows
    position = cyton.get_position()
    name = cyton.get_joint_names()
    point_list = myfile.get_list()
    pressure = myfile.get_pressure_val()
    pressure_haptic = haptic.get_pressure_val()
    target_val = match.get_target()
    cyton_gripper.drawer(canvas)
    haptic_gripper.drawer(canvas)
    canvas.draw_line((500, 0), (500, 600), 4, 'White')
    canvas.draw_text('Pressure Val ' + str(pressure), (10, 400), 30, 'White')
    canvas.draw_text('Haptic Pressure Val ' + str(pressure_haptic), (10, 500), 30, 'White')
    canvas.draw_text('Target Pressure Val ' + str(target_val),(10, 530), 30, 'White')
    canvas.draw_text('Stored Point', (510, 20), 30, 'White')
    for i in range(len(name)):
        canvas.draw_text(name[i] + ' Status: ' + str(position[i]), (10, 20 + 25 * i), 20, 'White')

    for i in range(len(point_list)):
        height = 40 + 18 * i - (variable.height) * weight
        if height > variable.height:
            width += 100
            weight += 1
        canvas.draw_text(str(point_list[i]), (width, height), 15, 'White')


# Definition for different classes
cyton_gripper = gripper([400, 400], [-1, 1])
haptic_gripper = gripper([400, 500], [80, 30])
variable = global_variable(600, 800)
match = matching()
cyton = arm(0.02)
myfile = pressure_storage('/dev/ttyACM1');
haptic = pressure_storage('/dev/ttyACM0');
robot = simplegui.create_frame("Cyton Controller Joystick", variable.width, variable.height, 80)
# Action to take before start
cyton.home()  # Should be placed before any 'Start' or there will be error
robot.add_input('File name', myfile.store_to_file, 50)
robot.set_draw_handler(draw)
main_timer = simplegui.create_timer(50, main)
pressure_timer = simplegui.create_timer(50, pass_pressure)
main_timer.start()
pressure_timer.start()
robot.start()
cyton.home()
