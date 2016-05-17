#!/usr/bin/env python

import serial
try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
nano = serial.Serial('/dev/ttyACM0',115200, timeout = 5)
#mega = serial.Serial('/dev/rfcomm2',9600)

def draw(canvas):
	temp = nano.readline()
	try:
		#pressure = float(nano.readline())
		pressure = float(temp)
		if pressure != 0:
			print pressure
			canvas.draw_text(str(pressure), (10, 20), 20, 'White')
			#canvas.draw_text(mega.readline(), (10, 40), 20, 'White')
	except Exception,e:
		print str(e) + str(temp)
	nano.flush()
	nano.flushInput()
	#nano.flushOutput()

Dev_Manager = simplegui.create_frame("Bluetooth tester", 300, 300)
Dev_Manager.set_draw_handler(draw)
Dev_Manager.start()

