'''
Program to save and store the formula from pressure sensor
Author: Qing Lan
Copyright: Free
Date: 1/2/2016
'''
import pygame  # function to configure the gamepad
import serial  # get the board data from serial port
import os  # use to store as a file
import time
import math
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import roslib  # Basic library for ROS

roslib.load_manifest('cyton_arm_controller')
from std_msgs.msg import Float64
import rospy  # ROS library for python
import matplotlib.pyplot as plt
import numpy as np

# initialize the environment
pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()
board = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
counter = 0  ##Only used in the auto_measure


############################## Center Variable controller
class global_variable:
    def __init__(self, height, width):
        # Basic information
        self.height = height
        self.width = width
        # determine the start of movement
        self.start = True
        self.select = False
        self.auto_measure = False
        self.auto_map = False
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
        self.move_position[7] = command[10] - command[11]
        # Red_button Start
        if (command[13] == 1):
            self.start = False
        else:
            self.start = True
        if (command[12] == 1):
            self.select = True
        else:
            self.select = False
        if (command[14] == 1):
            self.auto_measure = True
        if (command[15] == 1):
            self.auto_map = True

    def get_position(self):
        return self.move_position

    def get_start(self):
        return self.start

    def get_select(self):
        return self.select

    def get_auto_measure(self):
        return self.auto_measure

    def set_auto_measure(self, measure):
        self.auto_measure = measure

    def get_auto_map(self):
        return self.auto_map

    def set_auto_map(self, map_val):
        self.auto_map = map_val


################### Major movement controller
class arm:
    def __init__(self, move):
        # Position and Joint movement limits
        self.position = [0, 0, 0, 0, 0, 0, 0, -1]
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

    def get_joint_names(self):
        return self.joint_names

    def set_gripper(self, position):  # Really unsafe method to control the gripper, used by auto_move only
        self.position[7] = position


################################## Center of Pressure sensor data
class pressure_storage:
    def __init__(self):
        self.pressure_val = 0
        self.file_list = [[0, 0]]

    def get_pressure_val(self):
        return self.pressure_val

    def get_list(self):
        return self.file_list

    def pass_pressure(self):
        temp = board.readline()
        try:
            self.pressure_val = float(temp)
            print self.pressure_val
        except Exception, e:
            print str(e)
        board.flush()
        board.flushInput()

    def store_val(self, gripper_val):
        # if (self.pressure_val != self.file_list[-1][1]):
        self.file_list.append([gripper_val, self.pressure_val])

    def store_to_file(self, file_name):
        my_file = open(file_name, 'w')
        for i in range(len(self.file_list)):
            my_file.write(str(self.file_list[i][0]) + ',' + str(self.file_list[i][1]) + '\n')
        my_file.close()

    def clean_record(self):
        self.file_list = [[0, 0]]

    def get_file_list(self):
        return self.file_list


################################# Plotting result section
class plotting:
    def __init__(self):
        self.dataset = [[5, 0], [0, 1], [2, 3], [3, 2]]
        self.label_x = []
        self.label_y = []
        self.fit_result = [[0], [0], [0]]
        self.file_name = 'Rubber.txt'

    def from_file(self, file_name='Rubber.txt'):
        self.file_name = file_name
        self.label_x, self.label_y = np.loadtxt(self.file_name, delimiter=',', unpack=True)

    def from_device(self, data):
        self.dataset = data
        self.data_sort()
        self.transform()

    def transform(self):
        for i in range(len(self.dataset)):
            self.label_x.append(self.dataset[i][0])
            self.label_y.append(self.dataset[i][1])

    def data_sort(self):
        data = np.array(self.dataset)
        self.dataset = data[np.argsort(data[:, 0])]

    def plotgraph(self):
        plt.plot(self.label_x, self.label_y, 'ro')
        plt.axis([-1, 1, 0, 12])
        plt.show()

    def plotfitting(self):
        self.fitting()
        point = np.linspace(-1, 1, 100)
        p1 = np.poly1d(self.fit_result[0])
        p2 = np.poly1d(self.fit_result[1])
        p3 = np.poly1d(self.fit_result[2])
        plt.plot(self.label_x, self.label_y, 'ro', point, p1(point), 'g.', point, p2(point), 'b--', point, p3(point), '-')
        plt.axis([-1, 1, 0, 12])
        plt.show()

    def subplotfitting(self):
        self.fitting()
        point = np.linspace(-1, 1, 100)
        p1 = np.poly1d(self.fit_result[0])
        p2 = np.poly1d(self.fit_result[1])
        p3 = np.poly1d(self.fit_result[2])
        f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
        ax1.set_title(str("%.3f" % self.fit_result[0][0]) + ' + ' + str("%.3f" % self.fit_result[0][1]) + 'x')
        ax2.set_title(str("%.3f" % self.fit_result[1][0]) + ' + ' + str("%.3f" % self.fit_result[1][1]) + 'x + ' + str(
            "%.3f" % self.fit_result[1][2]) + 'x^2')
        ax3.set_title(str("%.3f" % self.fit_result[2][0]) + ' + ' + str("%.3f" % self.fit_result[2][1]) + 'x + ' + str(
            "%.3f" % self.fit_result[2][2]) + 'x^2 + ' + str("%.3f" % self.fit_result[2][3]) + 'x^3')
        ax1.plot(self.label_x, self.label_y, 'o', point, p1(point), 'g.')
        ax2.plot(self.label_x, self.label_y, 'o', point, p2(point), 'b--')
        ax3.plot(self.label_x, self.label_y, 'o', point, p3(point), '-')
        plt.xlabel('Displacement Value')
        plt.ylabel('Force Value')
        plt.axis([-1, 1, 0, 12])
        plt.show()

    def fitting(self):
        x = np.array(self.label_x)
        y = np.array(self.label_y)
        self.fit_result[0] = np.polyfit(x, y, 1)
        self.fit_result[1] = np.polyfit(x, y, 2)
        self.fit_result[2] = np.polyfit(x, y, 3)


################################ Gripper Class
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


def auto_store():
    global counter
    if variable.get_auto_measure():  ## When the button has pressed
        if counter == 0:  ## Initial mode
            cyton.set_gripper(-1)
            myfile.clean_record()
        elif counter <= 200:  ## Case when not at the end
            if myfile.get_pressure_val() <= 11:  ## case when pressure is too much
                value = -1 + counter * 0.01
                cyton.set_gripper(value)
                myfile.store_val(value)
            else:
                counter = 201
        else:  ## Final mode, move back
            counter = 0
            cyton.set_gripper(-1)
            variable.set_auto_measure(False)
        counter += 1
    if variable.get_auto_map():
        my_record.from_device(myfile.get_file_list())
        my_record.subplotfitting()
        variable.set_auto_map(False)


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


def main():
    variable.translation(joystick())
    select_result = variable.get_select()
    position = cyton.get_position()
    cyton_gripper.mapping(position[7], 0)
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
    canvas.draw_line((500, 0), (500, 600), 4, 'White')
    canvas.draw_text('Pressure Val ' + str(pressure), (10, 400), 30, 'White')
    canvas.draw_text('Stored Point', (510, 20), 30, 'White')
    cyton_gripper.drawer(canvas)
    for i in range(len(name)):
        canvas.draw_text(name[i] + ' Status: ' + str(position[i]), (10, 20 + 25 * i), 20, 'White')

    for i in range(len(point_list)):
        height = 40 + 18 * i - (variable.height) * weight
        if height > variable.height:
            width += 100
            weight += 1
        canvas.draw_text('[' + str("%.2f" % point_list[i][0]) + ',' + str("%.2f" % point_list[i][1]) + ']',
                         (width, height), 15, 'White')


variable = global_variable(600, 800)
my_record = plotting()  ##Map drawer
cyton_gripper = gripper([400, 400], [-1, 1])
cyton = arm(0.02)
myfile = pressure_storage();
robot = simplegui.create_frame("Cyton Controller Joystick", variable.width, variable.height, 100)

cyton.home()  # Should be placed before any 'Start' or there will be error
robot.add_input('File name', myfile.store_to_file, 50)
#################Timer section
robot.set_draw_handler(draw)
draw_timer = simplegui.create_timer(30, main)
pressure_timer = simplegui.create_timer(50, myfile.pass_pressure)
auto_measure = simplegui.create_timer(200, auto_store)
################# Get everything start to work
draw_timer.start()
pressure_timer.start()
auto_measure.start()
robot.start()
cyton.home()
