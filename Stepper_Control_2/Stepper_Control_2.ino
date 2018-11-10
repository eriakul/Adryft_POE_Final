// Stepper_Control combines serial port communication and stepper motor control. This is our main arduino script. 
// Import stepper motor libraries
#include <SpeedyStepper.h>

//const int MOTOR_STEP_PIN_X = 60;
//const int MOTOR_DIRECTION_PIN_X = 61;
//const int STEPPER_ENABLE_PIN_X = 56;
const int MOTOR_STEP_PIN_Y = 60; // for theta motor
const int MOTOR_DIRECTION_PIN_Y = 61;
const int STEPPER_ENABLE_PIN_Y = 56;
const int MOTOR_STEP_PIN_Z = 46; // for radius motor
const int MOTOR_DIRECTION_PIN_Z = 48;
const int STEPPER_ENABLE_PIN_Z = 62;

// Create two adafruit stepper motors, one on each port
// Create AccelStepper object for stepper driver with Step and Direction pins
SpeedyStepper stepper1;
SpeedyStepper stepper2;

// Create constant variables regarding mechanical system and stepper deg/step
const int RADIANS_TO_DEGREE = 360; // degrees in one revolution 
const float GEAR_RATIO = -4.69; // negative since gear spins opposite direction to motor
const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
const float FEET_TO_MM = 25.4*12; // multiply feet by this constant to get mm
const float MM_OFFSET = 1.25; // divide expected distance by constant to account for offset
//const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
const float DEG_PER_PEG = 7.5; // degree per peg to wrap string around

// Create constant variables read from python for wrapping string
//String WrapPairs[8];
float WrapCoordinates[6]; 
float wRadius1;
float wTheta1;
float wRadius2;
float wTheta2;

// Create variables for serial communication and computation
float Current_Pos = 0; 
String readString;
String radius1;
String theta1;
String direction1;
float radius2;
float theta2;
float direction2;

// moveStep takes in theta value and calculates how many relative revolutions stepper1 should make 
float moveRevolutions(float theta){
  // divide theta by deg/step to get number of steps 
  // negative corresponds to CCW and positive stands for CW
  float numRevo = theta/(RADIANS_TO_DEGREE/GEAR_RATIO);
  return numRevo;
}

// moveRadius takes in radius value and calculates how many mm (relative) stepper2 should move
float moveRadius(float radius){
  return radius*FEET_TO_MM;
}

// function to call motors to wrap string around the peg
void wrapString(String direction){
  if (direction.equals("N")){
      stepper2.setupRelativeMoveInMillimeters(WrapCoordinates[0]/MM_OFFSET); // move relative mm out from origin
      while(!stepper2.motionComplete())
      {
        stepper2.processMovement();
      }
      stepper1.setupRelativeMoveInRevolutions(WrapCoordinates[1]/RADIANS_TO_DEGREE); // move relative revolution counter clockwise 
      while(!stepper1.motionComplete())
      {
        stepper1.processMovement();
      }
      stepper2.setupRelativeMoveInMillimeters(WrapCoordinates[2]/MM_OFFSET); // move relative mm in towards origin
      while(!stepper2.motionComplete())
      {
        stepper2.processMovement();
      }
//      stepper1.setupRelativeMoveInRevolutions(WrapCoordinates[3]/RADIANS_TO_DEGREE); // move relative revolution clockwise
//      while(!stepper1.motionComplete())
//      {
//        stepper1.processMovement();
//      }
  }
  else if (direction.equals("S")){
      stepper2.setupRelativeMoveInMillimeters(WrapCoordinates[3]/MM_OFFSET); // move relative mm out from origin
      while(!stepper2.motionComplete())
      {
        stepper2.processMovement();
      }
      stepper1.setupRelativeMoveInRevolutions(WrapCoordinates[4]/RADIANS_TO_DEGREE); // move relative revolution counter clockwise 
      while(!stepper1.motionComplete())
      {
        stepper1.processMovement();
      }
      stepper2.setupRelativeMoveInMillimeters(WrapCoordinates[5]/MM_OFFSET); // move relative mm in towards origin
      while(!stepper2.motionComplete())
      {
        stepper2.processMovement();
      }
//      stepper1.setupRelativeMoveInRevolutions(WrapCoordinates[7]/RADIANS_TO_DEGREE); // move relative revolution clockwise
//      while(!stepper1.motionComplete())
//      {
//        stepper1.processMovement();
//      }
  }
}

void setup()
{  
    // Set up stepper motors
    // theta = stepper1
    pinMode(STEPPER_ENABLE_PIN_Y, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_Y,LOW);
    stepper1.connectToPins(MOTOR_STEP_PIN_Y, MOTOR_DIRECTION_PIN_Y);
    // radius = stepper2
    pinMode(STEPPER_ENABLE_PIN_Z, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_Z,LOW);
    stepper2.connectToPins(MOTOR_STEP_PIN_Z, MOTOR_DIRECTION_PIN_Z);
    
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
      int WrapCommandsIndex = readString.indexOf('W');
      if ( WrapCommandsIndex>=0 ){
        String WrapCommands = readString.substring(WrapCommandsIndex+1); 
        for(int i = 0; i < 6; i++){
          int colonIndex = WrapCommands.indexOf(';');
          String StrCoordinate= WrapCommands.substring(0, colonIndex);
          WrapCoordinates[i] = StrCoordinate.toFloat();
          WrapCommands = WrapCommands.substring(colonIndex+1);
        }
      }
      String commands = readString;
      int commaIndex = commands.indexOf(',');
      radius1 = commands.substring(0, commaIndex);
      commaIndex = commands.indexOf(',');
      theta1 = commands.substring(0,commaIndex);
      direction1 = commands.substring(commaIndex+1);
      // Convert strings to float
      radius2 = radius1.toFloat();
      theta2 = theta1.toFloat();
      // Set stepper1's target position according to theta value
      stepper1.setStepsPerRevolution(3200);
      stepper1.setSpeedInRevolutionsPerSecond(0.3);
      stepper1.setAccelerationInRevolutionsPerSecondPerSecond(0.3);
      stepper1.setupRelativeMoveInRevolutions(moveRevolutions(theta2));
      while(!stepper1.motionComplete())
      {
        stepper1.processMovement();
      }
      // Move stepper2
      stepper2.setStepsPerMillimeter(100); // set the number of steps per millimeter
      stepper2.setSpeedInMillimetersPerSecond(50); // set the speed in mm/sec
      stepper2.setAccelerationInMillimetersPerSecondPerSecond(40); // set the acceleration in mm/sec^2
//      stepper2.setupRelativeMoveInMillimeters(-moveRadius(radius2)/MM_OFFSET); // move relative mm
//      while(!stepper1.motionComplete()||!stepper2.motionComplete())
//      {
//        stepper2.processMovement();
//        stepper1.processMovement();
//      }
      wrapString(direction1);
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
