import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import time
import os 	#use to store as a file
import serial

board = serial.Serial('/dev/ttyACM0',9600, timeout = 5)

class pressure_storage:
    def __init__(self):
	self.pressure_val = 0.0
	self.file_list = []

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
	self.file_list.append([gripper_val,self.pressure_val])	
    
    def store_to_file(self, file_name):
	my_file = open(file_name, 'w')
	for i in range(len(self.file_list)):
		my_file.write(str(self.file_list[i][0]) + ',' + str(self.file_list[i][1]))
	my_file.close()

def store_the_file(textinput):
	myfile.store_val(1.5)
	myfile.store_to_file(textinput)

def draw(canvas):
	pass

def main():
	myfile.pass_pressure()
myfile = pressure_storage();
robot = simplegui.create_frame("Cyton Controller Joystick",600, 600, 80)
robot.add_input('File name', store_the_file, 50)
raw_timer = simplegui.create_timer(50, main)
robot.set_draw_handler(draw)
raw_timer.start()
robot.start()
