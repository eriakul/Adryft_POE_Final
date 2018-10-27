// Stepper_Control combines serial port communication and stepper motor control. This is our main arduino script. 
// Import stepper motor libraries
#include <AccelStepper.h>
#include <AFMotor.h>

// Create two adafruit stepper motors, one on each port
AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);
// Create constant variables regarding mechanical system and stepper deg/step
const float GEAR_RATIO = -5; // negative since gear spins opposite direction to motor
const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
// Create variables for serial communication and computation
float Current_Pos = 0; 
String readString;
String radius1;
String theta1;
float radius2;
float theta2;

// Forward and Backward functions for stepper motors
// Can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// Wrappers for the first motor!
void forwardstep1() {  
  motor1.onestep(FORWARD, SINGLE);
}
void backwardstep1() {  
  motor1.onestep(BACKWARD, SINGLE);
}
// Wrappers for the second motor!
void forwardstep2() {  
  motor2.onestep(FORWARD, SINGLE);
}
void backwardstep2() {  
  motor2.onestep(BACKWARD, SINGLE);
}

// Motor shield has two motor ports, wrap them in two AccelStepper objects
AccelStepper stepper1(forwardstep1, backwardstep1); // changes theta
AccelStepper stepper2(forwardstep2, backwardstep2); // changes r and used for string wrap

// moveStep takes in polar coordinate and calculates how many steps stepper1 should take 
float moveStep(float radius, float theta){
  // divide theta by deg/step to get number of steps 
  // negative corresponds to CCW and positive stands for CW
  float numStep = theta/(DEG_PER_STEP/GEAR_RATIO);
  return numStep;
}

void wrapString(){
  // function to call the top motor to wrap string around the peg
}

void setup()
{  
    // Set stepper motor speeds
    stepper1.setSpeed(50);
    stepper2.setSpeed(50);
    // Set up serial port
    Serial.begin(9600);  
}

void loop()
{
  while(!Serial.available()) {} // Do nothing if no message from python
  // Serial read section
  while (Serial.available())
  {
    if (Serial.available() > 0)
    {
      // Read in python message
      readString = Serial.readString();
      // Separate polar coordinate into radius and theta values
      int commaIndex = readString.indexOf(',');
      radius1 = readString.substring(0, commaIndex);
      theta1 = readString.substring(commaIndex + 1);
      // Convert strings to float
      radius2 = radius1.toFloat();
      theta2 = theta1.toFloat();
      // Set stepper1's target position according to theta value
      stepper1.moveTo(moveStep(radius2, theta2));
      // Move stepper1 until target position reached
      while (stepper1.distanceToGo() > 0){
        stepper1.runSpeed();
      }
      // Wrap string around peg
      wrapString();
    }
  }

  // If message received from python and motor finished moving, send return message to python
  if (readString.length() > 0)
  {
    Serial.print("Task Completed!");  
//    String radius3 = String(radius2*2);
//    String theta3 = String(theta2*2);
//    Serial.print(radius3); //see what was received
//    Serial.print(",");
//    Serial.println(theta3);
  }
  delay(500);
  Serial.flush(); //waits for transmission of outgoing serial data to complete
}
