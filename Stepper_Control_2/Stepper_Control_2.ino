// Stepper_Control combines serial port communication and stepper motor control. This is our main arduino script. 
// Import stepper motor libraries
#include <SpeedyStepper.h>

//const int MOTOR_STEP_PIN_X = 60;
//const int MOTOR_DIRECTION_PIN_X = 61;
//const int STEPPER_ENABLE_PIN_X = 56;
const int MOTOR_STEP_PIN_T = 60; // for theta motor
const int MOTOR_DIRECTION_PIN_T = 61;
const int STEPPER_ENABLE_PIN_T = 56;
const int MOTOR_STEP_PIN_R = 46; // for radius motor
const int MOTOR_DIRECTION_PIN_R = 48;
const int STEPPER_ENABLE_PIN_R = 62;
const int R_LIMIT_SWITCH_OUTPUT = 32; 

// Create two adafruit stepper motors, one on each port
// Create AccelStepper object for stepper driver with Step and Direction pins
SpeedyStepper stepper_t;
SpeedyStepper stepper_r;

// Create constant variables regarding mechanical system and stepper deg/step
const int REV_TO_DEGREE = 360; // degrees in one revolution 
const float GEAR_RATIO = -4.69; // negative since gear spins opposite direction to motor
const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
const float FEET_TO_MM = 25.4*12; // multiply feet by this constant to get mm
const float STEPS_PER_MM = 100/1.25; // divide expected distance by constant to account for offset
//const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
const float DEG_PER_PEG = 7.5; // degree per peg to wrap string around
const float RADIUS_IN_MM = 329.406; // distance from end of r axis to center

// Create constant variables read from python for wrapping string
float WrapCoordinates[6]; 

// Create variables for serial communication and computation
float Current_Pos = 0; 
String readString;
String radius1;
String theta1;
String direction1;
float radius2;
float theta2;
float direction2;

// moveStep takes in theta value and calculates how many relative revolutions stepper_t should make 
float moveRevolutions(float theta){
  // divide theta by deg/step to get number of steps 
  // negative corresponds to CCW and positive stands for CW
  float numRevo = theta/(REV_TO_DEGREE/GEAR_RATIO);
  return numRevo;
}

// moveRadius takes in radius value and calculates how many mm (relative) stepper_r should move
float moveRadius(float radius){
  return (radius*FEET_TO_MM/1.038);
}

// function to move r motors to center 
void toCenter(){
    stepper_r.setupRelativeMoveInMillimeters(RADIUS_IN_MM/1.038); // move relative mm
    while(!stepper_r.motionComplete())
    {
      stepper_r.processMovement();
    }
}

// function to call motors to wrap string around the peg
void wrapString(String direction1){
  if (direction1.equals("N")){
      stepper_r.setupRelativeMoveInMillimeters(-moveRadius(WrapCoordinates[0])); // move relative mm out from origin
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
      stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(WrapCoordinates[1])); // move relative revolution counter clockwise 
      while(!stepper_t.motionComplete())
      {
        stepper_t.processMovement();
      }
      stepper_r.setupRelativeMoveInMillimeters(-moveRadius(WrapCoordinates[2])); // move relative mm in towards origin
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
  }
  else if (direction1.equals("S")){
      stepper_r.setupRelativeMoveInMillimeters(-moveRadius(WrapCoordinates[3])); // move relative mm out from origin
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
      stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(WrapCoordinates[4])); // move relative revolution counter clockwise 
      while(!stepper_t.motionComplete())
      {
        stepper_t.processMovement();
      }
      stepper_r.setupRelativeMoveInMillimeters(-moveRadius(WrapCoordinates[5])); // move relative mm in towards origin
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
  }
}

void setup()
{  
    // Set up stepper motors
    // theta = stepper_t
    pinMode(STEPPER_ENABLE_PIN_T, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_T,LOW);
    stepper_t.connectToPins(MOTOR_STEP_PIN_T, MOTOR_DIRECTION_PIN_T);
    // radius = stepper_r
    pinMode(STEPPER_ENABLE_PIN_R, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_R,LOW);
    stepper_r.connectToPins(MOTOR_STEP_PIN_R, MOTOR_DIRECTION_PIN_R);

    //set up speed and acceleartion for stepper_t
    stepper_t.setStepsPerRevolution(3200);
    stepper_t.setSpeedInRevolutionsPerSecond(0.3);
    stepper_t.setAccelerationInRevolutionsPerSecondPerSecond(0.3);

    //set up speed and acceleartion for stepper_r
    stepper_r.setStepsPerMillimeter(STEPS_PER_MM); // set the number of steps per millimeter
    stepper_r.setSpeedInMillimetersPerSecond(70); // set the speed in mm/sec
    stepper_r.setAccelerationInMillimetersPerSecondPerSecond(50); // set the acceleration in mm/sec^2

// home the motor by moving until the homing sensor is activated, then set the position to zero
//    pinMode(R_LIMIT_SWITCH_OUTPUT, INPUT);
//    Serial.println("HOMING");
//    stepper_r.moveToHomeInMillimeters(-1, 20, 250, R_LIMIT_SWITCH_OUTPUT);
//    Serial.println("Found Home");
    
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
      if ( WrapCommandsIndex >= 0 ){
        String WrapCommands = readString.substring(WrapCommandsIndex+1); 
        for(int i = 0; i < 6; i++){
          int colonIndex = WrapCommands.indexOf(';');
          String StrCoordinate= WrapCommands.substring(0, colonIndex);
          WrapCoordinates[i] = StrCoordinate.toFloat();
          WrapCommands = WrapCommands.substring(colonIndex+1);
        }
        toCenter();
      }
      else{
        String commands = readString;
        int commaIndex = commands.indexOf(',');
        radius1 = commands.substring(0, commaIndex);
        commands = commands.substring(commaIndex+1);
        commaIndex = commands.indexOf(',');
        theta1 = commands.substring(0,commaIndex);
        direction1 = commands.substring(commaIndex+1);
        // Convert strings to float
        radius2 = radius1.toFloat();
        theta2 = theta1.toFloat();
        // Set stepper_t's target position according to theta value
        stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(theta2));
        // Move stepper_r
        stepper_r.setupRelativeMoveInMillimeters(-moveRadius(radius2)); // move relative mm
        while(!stepper_t.motionComplete()||!stepper_r.motionComplete())
        {
          stepper_r.processMovement();
          stepper_t.processMovement();
        }
        wrapString(direction1);
      }
    }
  
    if (readString.length() > 0)
    {
      Serial.println("Task Completed");
      readString = "";  
    }
    Serial.flush();
  }
}
