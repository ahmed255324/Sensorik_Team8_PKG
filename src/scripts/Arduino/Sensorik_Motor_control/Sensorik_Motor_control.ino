// Use the following line if you have a Leonardo or MKR1000
#define USE_USBCON
#include <Wire.h>
#include <Servo.h>                          //Include Servo Library
#include <ros.h>
#include <Sensorik_Team8_PKG/joy_axes.h>
#include <Sensorik_Team8_PKG/movecontrol.h>
#include <Sensorik_Team8_PKG/geschwindigkeit.h>
ros::NodeHandle nh;

//Tachometer
#define TACH_I2C_ADDRESS 0x11

Servo Servo_Motor;                          // Define Servo for the drive motor.
Servo Servo_Steer;                          // Define Servo for the steering motor

void messageCb( const Sensorik_Team8_PKG::joy_axes& move){
  Servo_Motor.write(map(move.motor, 100, -100, 180, 0));
  Servo_Steer.write(map(move.linker, -100, 100, 145, 20));
}

void messageCbc( const Sensorik_Team8_PKG::movecontrol& move){
  Servo_Motor.write(map(int(100*move.geschwindigkeit), 100, -100, 180, 0));
  Servo_Steer.write(map(int(100*move.lenkung), -100, 100, 145, 20));
}

ros::Subscriber<Sensorik_Team8_PKG::joy_axes> sub("/arduino_steuerung", &messageCb );
ros::Subscriber<Sensorik_Team8_PKG::movecontrol> subc("/movecontrol", &messageCbc );
Sensorik_Team8_PKG::geschwindigkeit g;
ros::Publisher gundm("/AutoGeschwindigkeit", &g);

void setup() 
{
  Wire.begin();
  Servo_Motor.attach(10, 0, 180);    // attach Pin 9 to motor with values 0 to 180 degrees (Servo angle degree)
  Servo_Motor.write(90);                    // Initialise servo at midpoint with 90 degrees
  Servo_Steer.attach(9, 0, 180);    // Attach Pin 7 to servo with values 0 to 180 degrees
  Servo_Steer.write(90);                    // Initialise servo at midpoint with 90 degrees
  nh.initNode();
  nh.subscribe(sub);
  nh.subscribe(subc);
  nh.advertise(gundm);
}

void loop() 
{
    Wire.requestFrom(TACH_I2C_ADDRESS, 4);    // request 4 bytes from slave device
    unsigned int temp = 0;
    for (int i = 0; i < 4; i++) {
    temp |= ((unsigned char)Wire.read() << (i * 8)); // respond with message of 4 bytes
    }
    g.Geschwindigkeit = (double)temp / 13107.0;
    gundm.publish(&g);
    nh.spinOnce();
}
