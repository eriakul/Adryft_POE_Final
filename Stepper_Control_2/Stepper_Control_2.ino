// Stepper_Control combines serial port communication and stepper motor control. This is our main arduino script. 
// Import stepper motor libraries
#include <SpeedyStepper.h>

const int RADIUS_TO_DEGREE = 360;
const int MOTOR_STEP_PIN_X = 60;
const int MOTOR_DIRECTION_PIN_X = 61;
const int STEPPER_ENABLE_PIN_X = 56;
const int MOTOR_STEP_PIN_Y = 60;
const int MOTOR_DIRECTION_PIN_Y = 61;
const int STEPPER_ENABLE_PIN_Y = 56;
// const int MOTOR_STEP_PIN_Z = ?;
// const int MOTOR_DIRECTION_PIN_Z = ?;
// const int STEPPER_ENABLE_PIN_Z = ?;

// Create two adafruit stepper motors, one on each port
// Create AccelStepper object for stepper driver with Step and Direction pins
SpeedyStepper stepper1;
SpeedyStepper stepper2;

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

// moveStep takes in polar coordinate and calculates how many steps stepper1 should take 
float moveRevolutions(float radius, float theta){
  // divide theta by deg/step to get number of steps 
  // negative corresponds to CCW and positive stands for CW
  float numRevo = theta/(RADIUS_TO_DEGREE/GEAR_RATIO);
  return numRevo;
}

void wrapString(){
  // function to call the top motor to wrap string around the peg
}

void setup()
{  
    // Set stepper motor speeds
    pinMode(STEPPER_ENABLE_PIN_Y, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_Y,LOW);
    stepper1.connectToPins(MOTOR_STEP_PIN_Y, MOTOR_DIRECTION_PIN_Y);
    // Set up serial port
    Serial.begin(9600);  
}

void loop()
{
  while(!Serial.available()) {} // Do nothing if no message from python
  // Serial read section
  while(Serial.available()){
    delay(30);
    if (Serial.available() > 0)
    {
      // Read in python message
      readString = Serial.readString();
      // Separate polar coordinate into radius and theta values
      int commaIndex = readString.indexOf(',');
      radius1 = readString.substring(0, commaIndex);
      theta1 = readString.substring(commaIndex+1);
      // Convert strings to float
      radius2 = radius1.toFloat();
      theta2 = theta1.toFloat();
      // Set stepper1's target position according to theta value
      stepper1.setStepsPerRevolution(3200);
      stepper1.setSpeedInRevolutionsPerSecond(1);
      stepper1.setupRelativeMoveInRevolutions(moveRevolutions(radius2, theta2));
       while(!stepper1.motionComplete())
      {
        stepper1.processMovement();
      }
    }
  
    if (readString.length() > 0)
    {
      Serial.print(theta1);
      Serial.println("Task Completed");
      readString = "";  
    }
  
    //delay(500);
    Serial.flush();
  }
}
