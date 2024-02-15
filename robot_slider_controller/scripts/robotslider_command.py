#!/usr/bin/env python3

import os
import sys
import signal
import time
import rospy
import requests
import json


from std_msgs.msg import String
from std_msgs.msg import Bool
import numpy as np

from robot_slider_controller.moveit_interface import robotplanninginterface 
#from moveit_interface import robotplanninginterface  

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def Points_from_AAS(url):
    response=requests.get(url)
    file_content = response.text
    ss=file_content.split(',')

    # Convert list of strings to list of floats
    float_list = [float(x) for x in file_content.split(',')]
    print(type(file_content))
    print(float_list)

    return float_list

url = ""

#joint_name =[slider_link_rail_stand_right_joint  - robot_stand_slider_joint   - joint_1 - joint_2  -joint_3 - joint_4 - joint_5 - joint_6]
#lower_j1_to_j6= [-3.14 -1.04 -2.30 -6.28 -2.18 -6.28] [-1.8 -pi/4]
#higher_j1_to_j6=[3.14 1.32 4.01 6.28 2.18 6.28] [21 pi]
def main():

    stand=robotplanninginterface("stand")
    stand.display_basic_info()
    rospy.loginfo("---------------------------------------------------")
    robot=robotplanninginterface("arm")
    robot.display_basic_info()
    stand1 = [2+4+5,2.8-1.5+1.5]
    #stand.go_to_joint_state(stand1)
    print(stand.move_group.get_current_joint_values())

    robot1=[-2, 1.1, -0, 0, -0, 0]
   # robot.go_to_joint_state(robot1)

#     time.sleep(1)
#     fanuc.move_group.get_current_joint_values()
    
    
#     test
#     #list_of_points =Points_from_AAS(url)

   
#     fanuc.go_to_joint_state(firstpoint_PCB)
    robot.go_to_pose_goal("x",0.1)
   




if __name__== "__main__":
    rospy.init_node("robot_stand_move_command", anonymous=True) 
    rospy.loginfo("The node robot_stand_move_command has been activated")
    rospy.loginfo("-----------------------------------------------------")
    main()
