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

from moveit_interface import robotplanninginterface

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

def main():

    fanuc=robotplanninginterface("arm_group")
    fanuc.display_basic_info()
    
    time.sleep(1)
    fanuc.move_group.get_current_joint_values()
    
    url="https://acbd-131-175-147-147.ngrok-free.app/shells/aHR0cHM6Ly9mYWJjdWJlLmV1L2lkcy9hYXMvZmFudWNyMjAwMGkxNjVm/submodels/aHR0cHM6Ly9mYWJjdWJlLmV1L2lkcy9zbS84MzMwXzgwMDJfMTAyMl8zMjIw/submodel-elements/AxisMovement.PositionFile/attachment"
    response=requests.get(url)
    file_content = response.text
    ss=file_content.splitlines()

    print(ss)
    # Convert list of strings to list of floats
    point_list_string = [x.split(',') for x in ss]
    print(point_list_string)
    point_list_float=[]
    for i in range(len(point_list_string)):
        a=[float(x) for x in point_list_string[i]]
        point_list_float.append(a)

    print(point_list_float)

    # with heating type gripper
    # firstpoint_PCB = [-0.7, 0.25, 0.2, -1.8, -0.5, 1.3]
    # firstpoint_PCB = float_list
    # with hand-e type gripper
    #firstpoint_PCB_hande = [1.4264733791351318, -1.2469455760768433, 1.7256587187396448, -2.0394584141173304, -1.5919478575335901, 4.490013599395752] 
    initial_joint_value=fanuc.move_group.get_current_joint_values()

    
    for i in range(len(point_list_string)):
        fanuc.go_to_joint_state(point_list_float[i])
        rospy.sleep(2)

   #fanuc.go_to_pose_goal("x",0.06)
   




if __name__== "__main__":
    rospy.init_node("fanuc_move", anonymous=True) 
    print("ddddd")
    main()
