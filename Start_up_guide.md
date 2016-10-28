# 2016-10-27 Guide to use the hands on module


## The runnable module CYTON Manager
create a file name "my_first_cyton.py" in desktop and put the following code. 
```python
import roslib  #Basic library for ROS
roslib.load_manifest('cyton_arm_controller')
from std_msgs.msg import Float64
import rospy #ROS library for python

def move(position):
        #core function in moving arm
        joint_commands = tuple(position)
	joint_names = ( 'shoulder_roll_controller', 'shoulder_pitch_controller', 'elbow_roll_controller',
        		'elbow_pitch_controller', 'wrist_roll_controller', 'wrist_pitch_controller',
        		'wrist_yaw_controller', 'gripper_open_controller')
        pubs = [rospy.Publisher(name + '/command', Float64) for name in joint_names]
	      rospy.init_node('cyton_veta', anonymous=True)
        for i in range(len(pubs)):
            pubs[i].publish(joint_commands[i])

my_position = [0,0,0,0,0,0,0,0]
move(my_position)
```
Then follow the guide in README.md to do roslaunch, after that run:
```
cd ~/Desktop
python my_first_cyton.py
```
Run this code will reset CYTON VETA to home position as straight up
## Multi-threading Introduction
This introduction will give you more views in the threading procedure

Find more information [Here](https://www.tutorialspoint.com/python/python_multithreading.htm)
### First Aid
If you happend to find that the system cannot find "threading" package
do the following:
```
pip install threading
```
Multithread is very useful when you want a program to run simutainiously without stopping. In this part, you will use thread Class. Create a file name "my_first_thread.py" on desktop and then run it (same as you run "my_first_cyton.py")
```python
import threading
import time

counter1 = 0
counter2 = 0

def th1():
    global counter1
    while counter1 < 20:
        print "Thread 2 runs " + str(counter1) +" times\n"
        counter1 += 1
        time.sleep(1)

def th2():
    global counter2
    while counter2 < 10:
        print "Thread 1 runs " + str(counter2) +" times\n"
        counter2 += 1
        time.sleep(2)

t1=threading.Thread(target = th1)
t2=threading.Thread(target = th2)

t1.start()
t2.start()
```
To call a thread you need the following, this is the minimal version of using thread. You need to maintain the code in my_running thread to create your own runnable thread.

```python
import threading  # thread class
import time	  # Time module

def my_running_thread():
	# main code here
	# pig_can_fly = true
	# while pig_can_fly:
	# 	print("Lanking is smart")
	time.sleep(1)
	pass
thread1=threading.Thread(target = my_running_thread) # Create a new thread
thread1.start() # Start the thread operation
```
## Gamepad module added
This is the minimum workable version of gamepad. To get it work properly, you need to press "Analog" on the gamepad.
```python
import pygame
import time

pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()

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
while True:
	print str(joystick()) + "\n"
	time.sleep(1)
```
## Get them work together
I have prepared a draft file for you, name it "My_First_Cyton_Controller.py" and put it on the desktop.

REMEBER to fix the format problem!

After your implementation, run roslauch first. Then open another terminal to run this code.
```python
import roslib  #Basic library for ROS
roslib.load_manifest('cyton_arm_controller')
from std_msgs.msg import Float64
import rospy #ROS library for python
import pygame
import time
import threading

pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()

# Global Variable
my_position = [0,0,0,0,0,0,0,0]
my_gamepad_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def move(position):
        #core function in moving arm
        joint_commands = tuple(position)
	joint_names = ( 'shoulder_roll_controller', 'shoulder_pitch_controller', 'elbow_roll_controller',
        		'elbow_pitch_controller', 'wrist_roll_controller', 'wrist_pitch_controller',
        		'wrist_yaw_controller', 'gripper_open_controller')
        pubs = [rospy.Publisher(name + '/command', Float64) for name in joint_names]
	rospy.init_node('cyton_veta', anonymous=True)
        for i in range(len(pubs)):
            pubs[i].publish(joint_commands[i])
	    
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

# Todo:
# 1. maintain the thread that can take out joystick data to global variable every 200ms.
def send_joypad_update_to_global():
	global my_gamepad_data
	while True:
        	# Your code Start here
		print str(my_gamepad_data)
        	time.sleep(0.2)

# Todo:
# 2. maintain the thread that can get the CYTON_VETA listen to the gamepad
def cyton_veta_to_game_pad():
	global my_gamepad_data, my_position
	while True:
		#Your code start here
		# my_position[3] += 0.05 * my_gamepad_data[0] # this line will let elbow_roll_controller follow the gamepad
		time.sleep(0.2)
# Todo:
# 3. can you tell me which one is the "Scale" in this function (how much I want the cyton move with game_pad data)

my_thread1=threading.Thread(target = send_joypad_update_to_global)
my_thread2=threading.Thread(target = cyton_veta_to_game_pad)
my_thread1.start()
my_thread2.start()
```
