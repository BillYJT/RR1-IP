#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include "ursa.srv"
int main(int argc, char** argv)
{
    ros::init(argc, argv, "lander");
    ros::NodeHandle n;
    ROS_INFO("Attempting Landing...\n");
    ursa::TakeoffLand srv;
    srv.request.takeoff = 0;
    if (_takeoff_service.call(srv)) {
        ROS_INFO("Success!");
    } else {
        ROS_ERROR("Failed to call service!");
    }
}
