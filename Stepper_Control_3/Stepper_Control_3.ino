// Stepper_Control combines serial port communication and stepper motor control. This is our main arduino script. 
// Import stepper motor libraries
#include <SpeedyStepper.h>

const int RADIANS_TO_DEGREE = 360;
//const int MOTOR_STEP_PIN_X = 60;
//const int MOTOR_DIRECTION_PIN_X = 61;
//const int STEPPER_ENABLE_PIN_X = 56;
const int MOTOR_STEP_PIN_Y = 60; // for theta motor
const int MOTOR_DIRECTION_PIN_Y = 61;
const int STEPPER_ENABLE_PIN_Y = 56;
const int MOTOR_STEP_PIN_Z = 46; // for radius motor
const int MOTOR_DIRECTION_PIN_Z = 48;
const int STEPPER_ENABLE_PIN_Z = 62;
const int R_LIMIT_SWITCH_OUTPUT = 32;   // Theta Limit Swtich

// Create two adafruit stepper motors, one on each port
// Create AccelStepper object for stepper driver with Step and Direction pins
SpeedyStepper stepper_t;
SpeedyStepper stepper_r;

// Create constant variables regarding mechanical system and stepper deg/step
const float GEAR_RATIO = -4.69; // negative since gear spins opposite direction to motor
const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
const float DEG_PER_PEG = 7.5; // degree per peg to wrap string around
const float INCH_TO_MM = 25.4; // multiply inch by this constant to get mm
const float MM_OFFSET = 1.25; // divide expected distance by constant to account for offset
// Create variables for serial communication and computation
float Current_Pos = 0; 
String readString;
String radius1;
String theta1;
float radius2;
float theta2;

// moveStep takes in theta value and calculates how many relative revolutions stepper_t should make 
float moveRevolutions(float theta){
  // divide theta by deg/step to get number of steps 
  // negative corresponds to CCW and positive stands for CW
  float numRevo = theta/(RADIANS_TO_DEGREE/GEAR_RATIO);
  return numRevo;
}

// moveRadius takes in radius value and calculates how many mm (relative) stepper_r should move
float moveRadius(float radius){
  return radius*INCH_TO_MM;
}

void wrapString(){
  // function to call the top motor to wrap string around the peg
      stepper_r.setupRelativeMoveInMillimeters(50/MM_OFFSET); // move relative mm out from origin
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
      stepper_t.setupRelativeMoveInRevolutions(DEG_PER_PEG/RADIANS_TO_DEGREE); // move relative revolution counter clockwise 
      while(!stepper_t.motionComplete())
      {
        stepper_t.processMovement();
      }
      stepper_r.setupRelativeMoveInMillimeters(-50/MM_OFFSET); // move relative mm in towards origin
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
      stepper_t.setupRelativeMoveInRevolutions(-DEG_PER_PEG/RADIANS_TO_DEGREE); // move relative revolution clockwise
      while(!stepper_t.motionComplete())
      {
        stepper_t.processMovement();
      }
}

void setup()
{  
    // Set stepper motors
    // theta = stepper_t
    pinMode(STEPPER_ENABLE_PIN_Y, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_Y,LOW);
    stepper_t.connectToPins(MOTOR_STEP_PIN_Y, MOTOR_DIRECTION_PIN_Y);
    // radius = stepper_r
    pinMode(STEPPER_ENABLE_PIN_Z, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_Z,LOW);
    stepper_r.connectToPins(MOTOR_STEP_PIN_Z, MOTOR_DIRECTION_PIN_Z);
    
    pinMode(R_LIMIT_SWITCH_OUTPUT, INPUT_PULLUP);
    
    // Set up serial port
    Serial.begin(9600);

    stepper_t.setStepsPerRevolution(3200);
    stepper_t.setSpeedInRevolutionsPerSecond(0.3);
    stepper_t.setAccelerationInRevolutionsPerSecondPerSecond(0.3);
    stepper_r.setStepsPerMillimeter(100); // set the number of steps per millimeter
    stepper_r.setSpeedInMillimetersPerSecond(40); // set the speed in mm/sec
    stepper_r.setAccelerationInMillimetersPerSecondPerSecond(30); // set the acceleration in mm/sec^2

    Serial.println("HOMING");
//    for (int i = 0; i < 30; i++) {
//     Serial.println(digitalRead(R_LIMIT_SWITCH_OUTPUT));
//     delay(1000);
//    }

    stepper_r.moveToHomeInMillimeters(-1, 20, 250, R_LIMIT_SWITCH_OUTPUT);
    
    Serial.println("found home");
}

void loop()
{
  exit(0);
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
      // Set stepper_t's target position according to theta value
      
      stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(theta2));
       while(!stepper_t.motionComplete())
      {
        stepper_t.processMovement();
      }
      // Move stepper_r
//      stepper_r.setupRelativeMoveInMillimeters(moveRadius(radius2)/MM_OFFSET); // move relative mm
//      while(!stepper_r.motionComplete())
//      {
//        stepper_r.processMovement();
//      }
       wrapString(); //wrap string around peg
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
