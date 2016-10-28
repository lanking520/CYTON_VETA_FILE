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
## Multiple threading Introduction
This introduction will give you more views in the threading procedure
Find more information [Here](https://www.tutorialspoint.com/python/python_multithreading.htm)

