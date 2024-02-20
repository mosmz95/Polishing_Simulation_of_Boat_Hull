#!/usr/bin/env python3

# edited by: Mostafa 

import argparse
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import numpy as np
import signal
from std_msgs.msg import Bool
import os
import time

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def all_close(goal, actual, tolerance):
    """
    Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
    @param: goal       A list of floats, a Pose or a PoseStamped
    @param: actual     A list of floats, a Pose or a PoseStamped
    @param: tolerance  A float
    @returns: bool
    """
    all_equal = True
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False

    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

    return True


class robotplanninginterface:
    """ Move Group Python Inteface """

    def __init__(self,groupName):
        #super(MoveGroupPythonIntefaceTutorial, self).__init__()

        
        moveit_commander.roscpp_initialize(sys.argv)
        #rospy.init_node('move_group_python_interface_mostafa', anonymous=True)

        
        robot = moveit_commander.RobotCommander()

        
        scene = moveit_commander.PlanningSceneInterface()

        
        self.group_name = groupName
        move_group = moveit_commander.MoveGroupCommander(self.group_name)

        # Create a `DisplayTrajectory`_ ROS publisher which is used to display
        # trajectories in Rviz:
        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                       moveit_msgs.msg.DisplayTrajectory,
                                                       queue_size=20)

        # END_SUB_TUTORIAL

        # Misc variables
        
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = move_group.get_planning_frame()
        self.eef_link = move_group.get_end_effector_link()
        self.group_names = robot.get_group_names()

    def display_basic_info(self):
        
        # Getting Basic Information
        # ^^^^^^^^^^^^^^^^^^^^^^^^^
        # We can get the name of the reference frame for this robot:
        print("============ Planning frame: %s" % self.planning_frame)

        # We can also print the name of the end-effector link for this group:
        print("============ End effector link: %s" % self.eef_link)

        # We can get a list of all the groups in the robot:
        print("============ Available Planning Groups:", self.group_names)

        # Sometimes for debugging it is useful to print the entire state of the
        # robot:
        print("============ Printing robot state")
        print(self.robot.get_current_state())
        print("")
        # END_SUB_TUTORIAL

    def go_to_joint_state(self,Jointgoal,angeltype="rad"):
        
        move_group = self.move_group

        # We can get the joint values from the group and adjust some of the values:
        joint_goal = move_group.get_current_joint_values()
        if angeltype=="rad":
            for i in range(0,len(joint_goal)):
                joint_goal[i] = Jointgoal[i]
        elif angeltype=="deg":
            for i in range(0,len(joint_goal)):
                joint_goal[i] = Jointgoal[i]*pi/180
        else:
            rospy.logerr("Invalid angle type: it should be ""rad"" or ""deg"" ")
            return False
    
        
        move_group.go(joint_goal, wait=True)

        # Calling ``stop()`` ensures that there is no residual movement
        move_group.stop()

      

        # For testing:
        print("Current pose", move_group.get_current_pose().pose)
        current_joints = move_group.get_current_joint_values()
        return all_close(joint_goal, current_joints, 0.01)

    def go_to_pose_goal(self,axis,magnitude):
        
        move_group = self.move_group
        
        # We can plan a motion for this group to a desired pose for the
        # end-effector:
        
            
        pose_goal = move_group.get_current_pose().pose
        if axis=="x" or axis=="X":
            pose_goal.position.x += magnitude
            rospy.loginfo("Moving the endeffector along  X axis")
        elif axis =="y" or axis=="Y":
            pose_goal.position.y += magnitude
            rospy.loginfo("Moving the endeffector along  Y axis")
        elif axis =="z" or axis=="Z":
            pose_goal.position.z += magnitude
            rospy.loginfo("Moving the endeffector along  Z axis")
            
        
        move_group.set_pose_target(pose_goal)
        
        plan = move_group.go(wait=True)
        
        move_group.stop()
        
        move_group.clear_pose_targets()
        
        
        current_pose = self.move_group.get_current_pose().pose
        return all_close(pose_goal, current_pose, 0.01)

        

    def plan_cartesian_path(self, scale=1):
        
        move_group = self.move_group

        
        waypoints = []

        wpose = move_group.get_current_pose().pose
        wpose.position.z -= scale * 0.1  # First move up (z)
        wpose.position.y += scale * 0.2  # and sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.y -= scale * 0.1  # Third move sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        
        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints,   # waypoints to follow
            0.01,        # eef_step
            0.0)         # jump_threshold

        # Note: We are just planning, not asking move_group to actually move the robot yet:
        return plan, fraction

        # END_SUB_TUTORIAL

    def display_trajectory(self, plan):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        robot = self.robot
        display_trajectory_publisher = self.display_trajectory_publisher

        
        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = robot.get_current_state()
        display_trajectory.trajectory.append(plan)
        # Publish
        display_trajectory_publisher.publish(display_trajectory)

        # END_SUB_TUTORIAL

    def execute_plan(self, plan):
        
        move_group = self.move_group

        
        move_group.execute(plan, wait=True)

        





            
   




