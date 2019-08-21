export ROS_MASTER_URI="http://127.0.0.1:11311"
export ROS_IP=127.0.0.1
source devel/setup.bash
#comment by guoxin 05/08
#roslaunch ursa new_ursa_sim.launch 
roslaunch ursa ursa_sim_takeoff_and_land.launch
