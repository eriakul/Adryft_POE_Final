#include <SpeedyStepper.h>

// Create AccelStepper object for stepper driver with Step and Direction pins
const int MOTOR_STEP_PIN_X = 54;
const int MOTOR_DIRECTION_PIN_X = 55;
const int STEPPER_ENABLE_PIN_X = 38;
const int MOTOR_STEP_PIN_Y = 60;
const int MOTOR_DIRECTION_PIN_Y = 61;
const int STEPPER_ENABLE_PIN_Y = 56;
const int MOTOR_STEP_PIN_Z = 46; // for radius motor
const int MOTOR_DIRECTION_PIN_Z = 48;
const int STEPPER_ENABLE_PIN_Z = 62;

SpeedyStepper Xaxis; // pin 54 = step, pin 55 = direction
SpeedyStepper Yaxis; // pin 60 = step, pin 61 = direction 
SpeedyStepper Zaxis;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Stepper test!");
  
  // set stepper motor speeds
  pinMode(STEPPER_ENABLE_PIN_X, OUTPUT);
  digitalWrite(STEPPER_ENABLE_PIN_X,LOW);
  pinMode(STEPPER_ENABLE_PIN_Y, OUTPUT);
  digitalWrite(STEPPER_ENABLE_PIN_Y,LOW);
  Xaxis.connectToPins(MOTOR_STEP_PIN_X, MOTOR_DIRECTION_PIN_X);
  Yaxis.connectToPins(MOTOR_STEP_PIN_Y, MOTOR_DIRECTION_PIN_Y);

  pinMode(STEPPER_ENABLE_PIN_Z, OUTPUT);
  digitalWrite(STEPPER_ENABLE_PIN_Z,LOW);
  Zaxis.connectToPins(MOTOR_STEP_PIN_Z, MOTOR_DIRECTION_PIN_Z);
}

void loop() {
  // put your main code here, to run repeatedly:
//  Xaxis.setSpeedInStepsPerSecond(100);
//  Xaxis.setAccelerationInStepsPerSecondPerSecond(100);
//  Xaxis.moveRelativeInSteps(-200);
  
//  Zaxis.setStepsPerRevolution(200);
//  Zaxis.setSpeedInRevolutionsPerSecond(1);
  // Xaxis.setAccelerationInRevolutionsPerSecondPerSecond(1); //why is acceleration 1 shouldn't it be 0 to be have constant speed?
//  Zaxis.setupRelativeMoveInRevolutions(1);
//  Xaxis.moveRelativeInRevolutions(1);
  
//  Yaxis.setStepsPerRevolution(3200);
//  Yaxis.setSpeedInRevolutionsPerSecond(1);
  //Yaxis.setAccelerationInRevolutionsPerSecondPerSecond(1);
//  Yaxis.setupRelativeMoveInRevolutions(1);

  Xaxis.setStepsPerRevolution(800);
  Xaxis.setSpeedInRevolutionsPerSecond(1);
  Xaxis.setupRelativeMoveInRevolutions(1);
  
  //Yaxis.moveRelativeInRevolutions(1);
//  delay(500);
//  Xaxis.moveRelativeInRevolutions(-1.5);
//    while((!Yaxis.motionComplete()) || (!Xaxis.motionComplete()))
//    {
//      Yaxis.processMovement();
//      Xaxis.processMovement();
//    }

      while(!Xaxis.motionComplete())
    {
      Xaxis.processMovement();
    }
}
