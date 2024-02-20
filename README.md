## Instruction


### Building the workspace:
1. Create a directory for the workspace:

```bash
  mkdir robotslider_ws
```
2. Go to the source directory of the workspace and clone the repository

```bash
cd robotslider_ws   
git clone https://github.com/mosmz95/Polishing_Simulation_of_Boat_Hull.git src
```
3. Build the workspace:

```bash 
  cd robotslider_ws
  catkin build
```
4. source the created workspace in the .bashrc file:

```bash
  echo "source robotslider_ws/devel/setup.bash" >> ~/.bashrc
  source ~/.bashrc
```

otherwise, it is required to source the workspace whenever a new terminal is open.



## Procedure to launch the Simulation environments

##### Visualization:  
The robot-slider movement is visualized in Rviz where by changing the slide-bar for each joint, you can see the range of motion of the corresponding joint.
```bash
  roslaunch robot_slider_description rviz_launch.launch 
```

##### Simulation of robot-slider motion: 

Gazebo software is a physics engine in which according to physical properties -like mass,intertia,etc, defined in urdf file- the dynamics of robot-slider movement is simulated. In fact, gazebo is a substitution of actual robot-slider. 

1. To launch the gazebo, run the following line in a new terminal:

```bash
  roslaunch robot_slider_bringup gazebo_launch.launch gui:=true
```
  In case you don't want to see grafical user interface, rewrite ``` gui:=false```

2. Launch the controller:

```bash
  roslaunch robot_slider_controller controller.launch
```

3. Launch the move_group which does the joint trajectory planning:  

```bash 
  roslaunch robot_slider_moveit move_group.launch
```

Depending on your system, it may take some time for the move_group to become ready to receive commands. You should see confirmation of this in the terminal "<span style="color:green;">You can start planning now!</span>"

4. To do trajectory plainning graphically, launch Rviz:

```bash 
  roslaunch robot_slider_description rviz_trajectoryplanning_launch.launch
```

5. if the desired joint positions are known in advance, you can edit the python file  ```robotslider_command.py``` inside the  robot_slider_controller package, then execute it:
```bash
  rosrun robot_slider_controller robotslider_command.py
```

##### Trajectory planning in Rviz


In this section, we briefly explain the procedure of joint trajetory planning. It is required to choose (i) a planning group, (ii) a start state (iii) a goal state. 

<div style="text-align:center;">
<img src="https://github.com/mosmz95/Polishing_Simulation_of_Boat_Hull/blob/master/photos/M1.png" alt="Alt text" width="300"/>
</div>
In the robot-slider mechansim, two planning goups are defined, namely "arm" and "stand", the former refers to th robot movement itself, and the latter refers to the linear and rotational  movements of slider-stand. 
The start state should be recieved from the gazebo(physics engine) and the goal state should be determined by the user. To do so, click on the "Joints" tab, then by moving the slider, choose the desired joint poistions as a goal state.
<div style="text-align:center;">
<img src="https://github.com/mosmz95/Polishing_Simulation_of_Boat_Hull/blob/master/photos/arm_joint.png" alt="Alt text" width="300"/>
</div>
In the next step, switch to the "Planning" tab and click on the "Planning" button to visulaize the movement from the start state to the goal state. In the end, to see the movement on the gazeboo, click on the "Execute" button. 