### ROS Installation on Ubuntu

 

1. Configure the Ubuntu repositories to allow "restricted," "universe," and "multiverse" repositories:  

```bash
sudo add-apt-repository universe
sudo add-apt-repository multiverse
sudo apt update
```
2. Setup your sources.list:  

Setup your computer to accept software from packages.ros.org.
```bash
  sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```
3. Set up your keys:  

```bash
  sudo apt install curl # if you haven't already installed curl
  curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
  ```
4. Update Debian packages:  