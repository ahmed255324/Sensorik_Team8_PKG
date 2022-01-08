// Wire Master Reader
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Reads data from an I2C/TWI slave device
// Refer to the "Wire Slave Sender" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>

//Tachometer
#define TACH_I2C_ADDRESS 0x11
double vehicleSpeed = 0.0;

double getVehicleSpeed();

void setup() {
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
}

void loop() {
  Serial.print(getVehicleSpeed());
  delay(1000);
}

double getVehicleSpeed() {
  double returnValue = -1;
  Wire.requestFrom(TACH_I2C_ADDRESS, 4);    // request 4 bytes from slave device
  if (Wire.available() == 4) { // slave may send less bytes than requested

    //double vehicleSpeedSmooth is a 32 bit floating point number; Wire.write()/Wire.read() expects singular bytes.
    //the double value will be cast into an unsigned int, multiplied with max_int/5, split into four individual bytes
    // which are then transmitted, to be assembled into an int, then a double again.
    unsigned int temp = 0;
    for (int i = 0; i < 4; i++) {
      temp |= ((unsigned char)Wire.read() << (i * 8)); // respond with message of 4 bytes
    }
    returnValue = (double)temp / 13107.0;

  }
  return returnValue;
}
