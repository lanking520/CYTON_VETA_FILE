#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import time

s = socket.socket()         # Create a socket object
host = '192.168.32.191' # Get local machine name
port = 12345                # Reserve a port for your service.
s.connect((host, port))

def network():
	about= list(eval(s.recv(1024)))
	print about
	#s.close                 

package_timer = simplegui.create_timer(50,network)
package_timer.start()
