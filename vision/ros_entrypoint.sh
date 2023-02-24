#!/bin/bash
set -e

# setup ros environment
source "/opt/ros/noetic/setup.bash" 
source "/opt/ros_ws/devel/setup.bash" 

# roslaunch zed_wrapper zed2i.launch
# roslaunch zed_display_rviz display_zed2i.launch    

exec "$@" # pass all arguments to the entrypoint