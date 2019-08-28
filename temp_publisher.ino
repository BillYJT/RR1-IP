#include <ros.h>
#include <std_msgs/String.h>
#include <sensor_msgs/LaserScan.h>

//std_msgs::String temp_msg;
ros::NodeHandle nh;
sensor_msgs::LaserScan temp_msg;
ros::Publisher pub_temp("temp", &temp_msg);

const int analog_pin = 0;
unsigned long timer = 0;
unsigned long publisher_timer = 0;

int dir_gen(int pin_num){
  return 1; //For testing, always detect in forward direction
}

char frameid[] = "temp_link";

void setup(){
  nh.initNode();
  nh.advertise(pub_temp);
  //Serial.begin(57600);

  temp_msg.header.frame_id =  frameid;
  temp_msg.angle_min = 0.0;
  temp_msg.angle_max = 6.28;  
  temp_msg.angle_increment = 6.28/20; 
  temp_msg.range_min = 0.03;  
  temp_msg.range_max = 7; 
  //temp_msg.scan_time = 0.05;
  temp_msg.ranges_length = 20;
  temp_msg.intensities_length = 20;
}

int num_readings = 20;

void loop(){
  int dir = dir_gen(analog_pin);
  float range[num_readings] = {0};
  float intensities[num_readings] = {0};
  int angle_start = (dir-1)*num_readings/4;
  int angle_end = dir*num_readings/4;

  if ( (millis()-publisher_timer) > 200){
    temp_msg.header.stamp = nh.now();
    timer =  millis();
    for(unsigned int i = angle_start; i < angle_end;  i++){
        range[i] = 1.0;
    }
     
    temp_msg.ranges = range;
    temp_msg.intensities = intensities;
    temp_msg.scan_time = millis() - timer;
    pub_temp.publish(&temp_msg);
    publisher_timer =  millis();
  }
  nh.spinOnce();
}
