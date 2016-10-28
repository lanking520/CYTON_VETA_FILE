# 2016-10-27 Guide to use the hands on module

## The runnable module
```python
def move(self):
        #core function in moving arm
        joint_commands = tuple(self.position)          
        pubs = [rospy.Publisher(name + '/command', Float64) for name in self.joint_names]
	      rospy.init_node('cyton_veta', anonymous=True)
        for i in range(len(pubs)):
            pubs[i].publish(joint_commands[i])
```
