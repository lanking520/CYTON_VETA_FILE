import time
import pygame
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import socket

out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
timer = 0
s = socket.socket()         # Create a socket object
host = '192.168.32.191'     # Get local machine IP
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.
c, addr = s.accept()     # Establish connection with client.
print 'Got connection from', addr

def network():
	print c.recv(1024)

package_timer = simplegui.create_timer(50,network)
package_timer.start()
