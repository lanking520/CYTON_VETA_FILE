import time
import pygame
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import socket

pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()

s = socket.socket()         # Create a socket object
host = '192.168.32.167'     # Get local machine IP
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

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

def network():
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    c.send(str(joystick()))

package_timer = simplegui.create_timer(50,network)
package_timer.start()
