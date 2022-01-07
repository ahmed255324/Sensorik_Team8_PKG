// Use the following line if you have a Leonardo or MKR1000
#define USE_USBCON
#include <Servo.h>                          //Include Servo Library
#include <ros.h>
#include <sensor_msgs/Joy.h>
#include <Sensorik_Team8_PKG/movecontrol.h>
ros::NodeHandle nh;

Servo Servo_Motor;                          // Define Servo for the drive motor.
Servo Servo_Steer;                          // Define Servo for the steering motor

void messageCb( const sensor_msgs::Joy& move){
  Servo_Motor.write(map(int(100*move.axes[1]), 100, -100, 180, 0));
  Servo_Steer.write(map(int(100*move.axes[3]), -100, 100, 145, 20));
}

void messageCbc( const Sensorik_Team8_PKG::movecontrol& move){
  Servo_Motor.write(map(int(100*move.geschwindigkeit), 100, -100, 180, 0));
  Servo_Steer.write(map(int(100*move.lenkung), -100, 100, 145, 20));
}

ros::Subscriber<sensor_msgs::Joy> sub("/joy", &messageCb );
ros::Subscriber<Sensorik_Team8_PKG::movecontrol> subc("/movecontrol", &messageCbc );

int PIN_Motor = 10;                         // Set PIN 9 as drive motor. 
int PIN_Steer = 9;                          // Set PIN 7 as steering motor.

void setup() 
{
  Servo_Motor.attach(PIN_Motor, 0, 180);    // attach Pin 9 to motor with values 0 to 180 degrees (Servo angle degree)
  Servo_Motor.write(90);                    // Initialise servo at midpoint with 90 degrees
  Servo_Steer.attach(PIN_Steer, 0, 180);    // Attach Pin 7 to servo with values 0 to 180 degrees
  Servo_Steer.write(90);                    // Initialise servo at midpoint with 90 degrees
  nh.initNode();
  nh.subscribe(sub);
  nh.subscribe(subc);
}

void loop() 
{  
    nh.spinOnce();
}