# Sensing Touch From a Robot Arm -- Qing's 2015-2016 Final Year Project

## General Description of The Project
The Robot with sensors’ feedback was becoming more significant in manufacturing, entertainment, medical areas in recent years. An important link to the feedback was the network among the machines and robots. Without the appropriate networks, the feedback from the robotic arm could be useless and even damage to the robotic system. This project focused on the force reflection from the robot arm and control it by using a joypad and Haptic Device. Network test applied after the system was finished. Two microcontrollers, two computers and a robot arm was the major hardware component used in the project. The final system design generally followed the operating system design rules with Processing Manager, Device Manager, Memory Manager, Network Manager and File Manager. Six different systems were built and 5 network models were tested to evaluate the performance of the Robotic Control system. Machine Learning, Forward and Inverse Kinematics and Robot Visualization was proved to be useful in the future system development.
## Some important things before you use
- You need ROS installed on your computer
- C and Python Environment required
- Rosbuild CYTON VETA Pacakge
- SimpleGUI replacement module required: Pygame, Matplotlib
- Additional module needed: Numpy, Pyserial
- Run Ros_start first to enable a node

## A startup guide for the user
This guide will help you to create a basic Running code
### Preparation
1. Get Cyton Veta connect to battery and check the usb terminal
2. Git clone this repository (Google how to do git clone) to the desktop
3. This tutorial will assume you have this file on the desktop
### Push ROS Node on the Computer
Create a terminal
```
cd ~/Desktop
cd CYTON_VETA_FILE/
cd ROS_Start/
roslaunch cyton_veta.launch.usb0
```
Alternatively, you can do
```
roslaunch ~/Desktop/CYTON_VETA_FILE/ROS_Start/CYTcyton_veta.launch.usb0
```
### Run the python file you have created

