#include <SpeedyStepper.h>

// Create AccelStepper object for stepper driver with Step and Direction pins
const int MOTOR_STEP_PIN = 54;
const int MOTOR_DIRECTION_PIN = 55;
const int STEPPER_ENABLE_PIN = 38;

SpeedyStepper Xaxis; // pin 54 = step, pin 55 = direction

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Stepper test!");
  
  // set stepper motor speeds
  pinMode(STEPPER_ENABLE_PIN, OUTPUT);
  digitalWrite(STEPPER_ENABLE_PIN,LOW);
  Xaxis.connectToPins(MOTOR_STEP_PIN, MOTOR_DIRECTION_PIN);
}

void loop() {
  // put your main code here, to run repeatedly:
  Xaxis.setStepsPerRevolution(200);
  Xaxis.setSpeedInRevolutionsPerSecond(1);
  Xaxis.setAccelerationInRevolutionsPerSecondPerSecond(1);
  Xaxis.moveRelativeInRevolutions(1.5);
  delay(500);
  Xaxis.moveRelativeInRevolutions(-1.5);
  while (true);
}
