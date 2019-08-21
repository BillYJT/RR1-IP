export ROS_MASTER_URI="http://127.0.0.1:11311"
export ROS_IP=127.0.0.1
make posix_sitl_default
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/posix_sitl_default	
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo
roslaunch px4 posix_sitl2.launch
