#include <ros.h>
#include <std_msgs/String.h>
#include <sensor_msgs/LaserScan.h>

//std_msgs::String temp_msg;
ros::NodeHandle nh;
sensor_msgs::LaserScan temp_msg;
ros::Publisher pub_temp("temp", &temp_msg);

const int analog_pin = A0;
unsigned long timer = 0;
unsigned long publisher_timer = 0;
char str[20];
char result[8];
int num_readings = 10;

int dir_gen(int pin_num){
  return 1; //For testing, always detect in forward direction
}

char frameid[] = "temp_link";

void setup(){
  nh.initNode();
  nh.advertise(pub_temp);
  //Serial.begin(9600);

  temp_msg.header.frame_id =  frameid;
  temp_msg.angle_min = 0.0;
  temp_msg.angle_max = 0.52;  
  temp_msg.angle_increment = temp_msg.angle_max/num_readings; 
  temp_msg.range_min = 0.03;  
  temp_msg.range_max = 7; 
  //temp_msg.scan_time = 0.05;
  temp_msg.ranges_length = num_readings;
  temp_msg.intensities_length = num_readings;
}


void loop(){
  int dir = dir_gen(analog_pin);
  float range[num_readings] = {0};
  float intensities[num_readings] = {0};
  int angle_start = (dir-1)*num_readings/4;
  int angle_end = dir*num_readings/4;
  float val;
  if ( (millis()-publisher_timer) > 200){
    temp_msg.header.stamp = nh.now();
    timer =  millis();
    val = analogRead(A0);

    //print the analog read
    dtostrf(val, 6, 2, result);   //Convert float to String
    sprintf(str, "Value = %s", result); //Construct the char array, loginfo take char array instead of String
    nh.loginfo(str);              //Print to the terminal
    if (val < 0.03*1024){
      val = 0.03*1024;  
    }
    //Serial.println(val);
    if (val<100){
      for(unsigned int i = 0; i < num_readings;  i++){ //only place obstacles in front of drone
          range[i] = 60*val/1024;
      }
    } 
    temp_msg.ranges = range;
    temp_msg.intensities = intensities;
    temp_msg.scan_time = millis() - timer;
    pub_temp.publish(&temp_msg);
    publisher_timer =  millis();
  }
  nh.spinOnce();
}
