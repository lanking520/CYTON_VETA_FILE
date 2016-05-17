import time
import pygame
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import socket

pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()
out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
timer = 0
s = socket.socket()         # Create a socket object
host = '192.168.40.20' # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))

def joystick():
    global out
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

def network():
    global timer
    package = joystick()
    send_pac = False
    for i in range (len(package)-1):
	if(package[i] != 0 or package[i] != 0.0):
	    send_pac = True;
    if send_pac:
       timer += 1 # Count iterations
       package[16] = timer
       s.send(str(package))
       print package

package_timer = simplegui.create_timer(50,network)
package_timer.start()
