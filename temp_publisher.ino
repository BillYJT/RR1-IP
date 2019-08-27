
#include <ros.h>
#include <std_msgs/String.h>
#include <sensor_msgs/LaserScan.h>

//std_msgs::String temp_msg;
ros::NodeHandle nh;
sensor_msgs::LaserScan temp_msg;
ros::Publisher pub_temp("temp", &temp_msg);

const int analog_pin = 0;
unsigned long timer;

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
  temp_msg.angle_increment = 3.14; 
  temp_msg.range_min = 0.03;  
  temp_msg.range_max = 7; 
  temp_msg.scan_time = 0.2;
  //temp_msg.ranges_length = 80;
}

int num_readings = 2;//(temp_msg.angle_max - temp_msg.angle_min)/temp_msg.angle_increment;

void loop(){
  int dir = dir_gen(analog_pin);
  float range[num_readings];

  if (1){   
    for(unsigned int i = 0; i < num_readings;  i++){
     
      temp_msg.ranges[i] = 6.0;
  
      nh.loginfo("aa");
    }
    
  }  
  //Need to add cases for other directions

  //for(unsigned int i = 0; i < num_readings; i++){
  //  temp_msg.ranges[i] =  range[i];
  //}
  
  temp_msg.header.stamp = nh.now();
  pub_temp.publish(&temp_msg);
  //timer =  millis();
  nh.spinOnce();
}