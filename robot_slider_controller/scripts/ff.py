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

   
    
    url="https://e466-131-175-147-147.ngrok-free.app/shells/aHR0cHM6Ly9mYWJjdWJlLmV1L2lkcy9hYXMvZmFudWNyMjAwMGkxNjVm/submodels/aHR0cHM6Ly9mYWJjdWJlLmV1L2lkcy9zbS84MzMwXzgwMDJfMTAyMl8zMjIw/submodel-elements/AxisMovement.PositionFile/attachment"
    response=requests.get(url)
    file_content = response.text
    ss=file_content.split(',')
    print(file_content)
    # Convert list of strings to list of floats
    # float_list = [float(x) for x in file_content.split(',')]
    print(type(file_content))
    print(type(ss))

    # with heating type gripper
   
print("ddddd")
main()

# if __name__== "main":
#     rospy.init_node("fanuc_move", anonymous=True) 
#     print("ddddd")
#     main()
