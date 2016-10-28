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
To call a thread you need the following
```python
import threading  # thread class
import time	  # Time module

def my_running_thread():
	# main code here
	pass
thread1=threading.Thread(target = my_running_thread) # Create a new thread
thread1.start() # Start the thread operation
```

